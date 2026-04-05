import re
from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.db import transaction

from pypdf import PdfReader

from questoes.models import Questao
from simulados.models import Simulado, SimuladoQuestao

from .models import ImportacaoProva, ProvaOriginal, QuestaoImportada, QuestaoProvaOriginal


QUESTION_LINE_RE = re.compile(
    r'^\s*(?:(?:Q\s*U\s*E\s*S\s*T\w*)\s+)?(\d{1,3})\s*$',
    re.IGNORECASE,
)
ALT_LINE_RE = re.compile(r'^\s*([A-E])(?:[\)\].:\-\s]|$)\s*(.*)$')
PAIR_RE = re.compile(r'\b(\d{1,3})\s*([A-E])\b')
PDF_HEADER_RE = re.compile(r'.*\|\s*\d.{0,2}\s*DIA\s*\|\s*CADERNO\s*\d+\s*\|\s*[A-Z]+.*', re.IGNORECASE)
BROKEN_WORD_RE = re.compile(r'^[a-zà-ÿ]{1,8}$', re.IGNORECASE)
BROKEN_WORD_SUFFIX_RE = re.compile(r'^(.*\b)([a-zà-ÿ]{1,6})$', re.IGNORECASE)
SECTION_BREAK_RE = re.compile(
    r'^(?:Texto para as QUESTAO|QUESTAO \d+\s+a\s+\d+|DA REDA|PROPOSTA DE REDA|LINGUAGENS,|CIÊNCIAS |CIENCIAS |MATEMÁTICA |MATEMATICA )',
    re.IGNORECASE,
)
WORD_ONLY_RE = re.compile(r'^[A-Za-zÀ-ÿ]+$')
JOIN_START_EXCEPTIONS = {'que'}
JOIN_START_STOPWORDS = {
    'a', 'as', 'ao', 'aos', 'o', 'os', 'de', 'da', 'das', 'do', 'dos', 'e',
    'em', 'na', 'nas', 'no', 'nos', 'um', 'uma', 'uns', 'umas', 'para', 'por',
    'com', 'sem', 'sob', 'sobre',
}


def is_pdf_noise_line(line):
    normalized = line.upper()
    if re.fullmatch(r'\*?[A-Z0-9]{6,}\*?', line):
        return True
    if 'ENEM2025' in normalized or '.INDB' in normalized or '.INDD' in normalized:
        return True
    if re.fullmatch(r'\d{1,2}', line):
        return True
    if PDF_HEADER_RE.fullmatch(line):
        return True
    if '|' in line and 'DIA' in normalized and 'CADERNO' in normalized:
        return True
    return False


def normalize_text(text):
    text = text.replace('\r', '\n')
    text = text.replace('\x00', ' ')
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'Q\s*U\s*E\s*S\s*T[^\d\n]{0,10}(\d{1,3})', r'QUESTAO \1', text, flags=re.IGNORECASE)
    lines = []
    for raw_line in text.splitlines():
        line = re.sub(r'\s+', ' ', raw_line).strip()
        if not line:
            continue
        if is_pdf_noise_line(line):
            continue
        lines.append(line)
    return '\n'.join(lines)


def clean_extracted_field(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = []

    for line in lines:
        if is_pdf_noise_line(line):
            continue
        if SECTION_BREAK_RE.match(line):
            break

        if cleaned:
            previous = cleaned[-1]
            if (
                BROKEN_WORD_RE.fullmatch(previous)
                and re.match(r'^[a-zà-ÿ]', line, re.IGNORECASE)
            ):
                cleaned[-1] = f'{previous}{line}'
                continue

            previous_match = BROKEN_WORD_SUFFIX_RE.match(previous)
            if previous_match and re.match(r'^[a-zà-ÿ]', line, re.IGNORECASE):
                cleaned[-1] = f'{previous_match.group(1)}{previous_match.group(2)}{line}'
                continue

        cleaned.append(fix_fragmented_start(line))

    return '\n'.join(cleaned).strip()


def fix_fragmented_start(line):
    parts = line.split()
    if len(parts) < 2:
        return line

    def is_word(token):
        return bool(WORD_ONLY_RE.fullmatch(token))

    def first_token_can_merge(token):
        return token.lower() not in JOIN_START_STOPWORDS or token.lower() in JOIN_START_EXCEPTIONS

    if len(parts) >= 3 and all(is_word(token) for token in parts[:3]):
        first, second, third = parts[:3]
        if len(first) == 1 and 1 <= len(second) <= 3 and len(third) >= 4:
            parts = [first + second + third, *parts[3:]]
            return ' '.join(parts)

    first, second = parts[:2]
    if all(is_word(token) for token in (first, second)):
        if len(first) <= 4 and len(second) >= 5 and first_token_can_merge(first):
            parts = [first + second, *parts[2:]]
            return ' '.join(parts)
        if 2 <= len(first) <= 4 and len(second) == 1 and first_token_can_merge(first):
            parts = [first + second, *parts[2:]]
            return ' '.join(parts)

    return line


def extract_pdf_text(file_field):
    file_field.open('rb')
    try:
        reader = PdfReader(file_field)
        pages = [(page.extract_text() or '') for page in reader.pages]
    finally:
        file_field.close()
    return normalize_text('\n'.join(pages))


def parse_gabarito(text):
    answers = OrderedDict()
    for numero, alternativa in PAIR_RE.findall(text):
        numero_int = int(numero)
        if 1 <= numero_int <= 200 and numero_int not in answers:
            answers[numero_int] = alternativa.upper()
    return answers


def split_question_blocks(text):
    blocks = OrderedDict()
    current_number = None
    current_lines = []

    for line in text.splitlines():
        match = QUESTION_LINE_RE.search(line)
        if match:
            number = int(match.group(1))
            if 1 <= number <= 200:
                if current_number is not None and current_lines:
                    blocks[current_number] = '\n'.join(current_lines).strip()
                current_number = number
                current_lines = []
                continue
        if current_number is not None:
            current_lines.append(line)

    if current_number is not None and current_lines:
        blocks[current_number] = '\n'.join(current_lines).strip()

    return blocks


def parse_question_block(block_text):
    lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    enunciado_lines = []
    alternatives = {letter: [] for letter in 'ABCDE'}
    current_letter = None

    candidate_indexes = []
    for idx, line in enumerate(lines):
        match = ALT_LINE_RE.match(line)
        if match:
            candidate_indexes.append((idx, match.group(1), match.group(2).strip()))

    candidate_sequences = []
    expected_letters = ['A', 'B', 'C', 'D', 'E']
    for idx, letter, _tail in candidate_indexes:
        if letter != 'A':
            continue

        found = {'A': idx}
        cursor = 1
        for next_idx, next_letter, _ in candidate_indexes:
            if next_idx <= idx:
                continue
            if next_letter == expected_letters[cursor]:
                found[next_letter] = next_idx
                cursor += 1
                if cursor == len(expected_letters):
                    candidate_sequences.append(found)
                    break

    start_indexes = None
    if candidate_sequences:
        start_indexes = min(
            candidate_sequences,
            key=lambda item: (item['E'] - item['A'], -item['A'])
        )

    if start_indexes:
        enunciado_lines = lines[:start_indexes['A']]
        for idx, line in enumerate(lines[start_indexes['A']:], start=start_indexes['A']):
            match = ALT_LINE_RE.match(line)
            if match and start_indexes.get(match.group(1)) == idx:
                current_letter = match.group(1)
                tail = match.group(2).strip()
                if tail:
                    alternatives[current_letter].append(tail)
                continue

            if current_letter is None:
                enunciado_lines.append(line)
            else:
                alternatives[current_letter].append(line)
    else:
        enunciado_lines = lines

    parsed = {
        'texto_bruto': block_text.strip(),
        'enunciado': clean_extracted_field('\n'.join(enunciado_lines)),
        'opcao_a': clean_extracted_field('\n'.join(alternatives['A'])),
        'opcao_b': clean_extracted_field('\n'.join(alternatives['B'])),
        'opcao_c': clean_extracted_field('\n'.join(alternatives['C'])),
        'opcao_d': clean_extracted_field('\n'.join(alternatives['D'])),
        'opcao_e': clean_extracted_field('\n'.join(alternatives['E'])),
    }
    return parsed


def classify_question(parsed, answer):
    problems = []
    if not parsed['enunciado']:
        problems.append('Enunciado nao foi extraido corretamente.')

    missing = [
        letter for letter, field in zip(
            'ABCDE',
            ['opcao_a', 'opcao_b', 'opcao_c', 'opcao_d', 'opcao_e'],
        )
        if not parsed[field]
    ]
    if missing:
        problems.append(f'Alternativas ausentes: {", ".join(missing)}.')

    if answer not in {'A', 'B', 'C', 'D', 'E'}:
        problems.append('Gabarito oficial ausente ou invalido.')

    status = (
        QuestaoImportada.CORRECAO_NECESSARIA if problems
        else QuestaoImportada.PENDENTE_APROVACAO
    )
    return status, ' '.join(problems)


def infer_expected_total(question_blocks, gabarito):
    return max(
        max(question_blocks.keys(), default=0),
        max(gabarito.keys(), default=0),
    )


def canonicalize_question_text(text):
    cleaned = clean_extracted_field(text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return cleaned


def find_existing_question(questao_importada):
    candidatos = Questao.objects.filter(
        resposta_correta=questao_importada.gabarito_oficial,
    )
    alvo = {
        'enunciado': canonicalize_question_text(questao_importada.enunciado),
        'opcao_a': canonicalize_question_text(questao_importada.opcao_a),
        'opcao_b': canonicalize_question_text(questao_importada.opcao_b),
        'opcao_c': canonicalize_question_text(questao_importada.opcao_c),
        'opcao_d': canonicalize_question_text(questao_importada.opcao_d),
        'opcao_e': canonicalize_question_text(questao_importada.opcao_e),
    }

    for candidato in candidatos:
        candidato_normalizado = {
            'enunciado': canonicalize_question_text(candidato.enunciado),
            'opcao_a': canonicalize_question_text(candidato.opcao_a),
            'opcao_b': canonicalize_question_text(candidato.opcao_b),
            'opcao_c': canonicalize_question_text(candidato.opcao_c),
            'opcao_d': canonicalize_question_text(candidato.opcao_d),
            'opcao_e': canonicalize_question_text(candidato.opcao_e),
        }
        if candidato_normalizado == alvo:
            return candidato

    return None


@transaction.atomic
def processar_importacao(importacao):
    importacao.status = ImportacaoProva.PROCESSANDO
    importacao.mensagem_erro = ''
    importacao.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])

    if not importacao.pdf_prova or not importacao.pdf_gabarito:
        raise ValidationError('Envie os PDFs da prova e do gabarito.')

    prova_texto = extract_pdf_text(importacao.pdf_prova)
    gabarito_texto = extract_pdf_text(importacao.pdf_gabarito)

    question_blocks = split_question_blocks(prova_texto)
    gabarito = parse_gabarito(gabarito_texto)

    if not question_blocks:
        raise ValidationError(
            'Nao foi possivel identificar questoes no PDF da prova. '
            'Verifique se o arquivo possui texto extraivel.'
        )
    if not gabarito:
        raise ValidationError(
            'Nao foi possivel identificar o gabarito no PDF enviado.'
        )

    max_gabarito = max(gabarito.keys(), default=0)
    if max_gabarito:
        question_blocks = OrderedDict(
            (numero, block)
            for numero, block in question_blocks.items()
            if numero <= max_gabarito
        )

    prova_original, _ = ProvaOriginal.objects.get_or_create(
        importacao=importacao,
        defaults={
            'descricao': (
                f'ENEM {importacao.ano} - Dia {importacao.dia} - '
                f'{importacao.get_cor_display()}'
            ),
        },
    )
    prova_original.descricao = (
        f'ENEM {importacao.ano} - Dia {importacao.dia} - {importacao.get_cor_display()}'
    )
    prova_original.total_questoes_esperado = infer_expected_total(question_blocks, gabarito)
    prova_original.status_editorial = ProvaOriginal.EM_REVISAO
    prova_original.save()

    simulado, _ = Simulado.objects.get_or_create(
        importacao_origem=importacao,
        defaults={
            'titulo': prova_original.descricao,
            'descricao': 'Simulado original importado de prova oficial do INEP.',
            'criado_por': importacao.criado_por,
            'ativo': False,
            'eh_simulado_original': True,
            'prova_original': prova_original,
        },
    )
    simulado.titulo = prova_original.descricao
    simulado.descricao = 'Simulado original importado de prova oficial do INEP.'
    simulado.criado_por = importacao.criado_por
    simulado.ativo = False
    simulado.eh_simulado_original = True
    simulado.prova_original = prova_original
    simulado.save()

    importacao.questoes_importadas.all().delete()

    created = []
    for numero, block in question_blocks.items():
        parsed = parse_question_block(block)
        answer = gabarito.get(numero, '')
        status, reason = classify_question(parsed, answer)
        created.append(
            QuestaoImportada(
                importacao=importacao,
                prova_original=prova_original,
                numero_na_prova=numero,
                texto_bruto=parsed['texto_bruto'],
                enunciado=parsed['enunciado'],
                opcao_a=parsed['opcao_a'],
                opcao_b=parsed['opcao_b'],
                opcao_c=parsed['opcao_c'],
                opcao_d=parsed['opcao_d'],
                opcao_e=parsed['opcao_e'],
                gabarito_oficial=answer,
                status=status,
                motivo_status=reason,
            )
        )
    QuestaoImportada.objects.bulk_create(created)

    importacao.status = ImportacaoProva.AGUARDANDO_REVISAO
    importacao.save(update_fields=['status', 'atualizado_em'])
    atualizar_status_importacao(importacao)
    return importacao


@transaction.atomic
def publicar_questao_importada(questao_importada):
    if questao_importada.status == QuestaoImportada.PUBLICADA:
        return questao_importada.questao_oficial

    if questao_importada.status == QuestaoImportada.REJEITADA:
        raise ValidationError('Questoes rejeitadas nao podem ser publicadas.')

    if not all([
        questao_importada.enunciado,
        questao_importada.opcao_a,
        questao_importada.opcao_b,
        questao_importada.opcao_c,
        questao_importada.opcao_d,
        questao_importada.opcao_e,
        questao_importada.gabarito_oficial,
    ]):
        raise ValidationError(
            'Preencha enunciado, alternativas A-E e gabarito oficial antes de publicar.'
        )

    questao = find_existing_question(questao_importada)
    if questao is None:
        questao = Questao.objects.create(
            enunciado=questao_importada.enunciado,
            opcao_a=questao_importada.opcao_a,
            opcao_b=questao_importada.opcao_b,
            opcao_c=questao_importada.opcao_c,
            opcao_d=questao_importada.opcao_d,
            opcao_e=questao_importada.opcao_e,
            resposta_correta=questao_importada.gabarito_oficial,
            dificuldade='M',
            explicacao='',
            fonte='ENEM oficial - INEP',
            ano_origem=questao_importada.importacao.ano,
            revisado=True,
            importacao_origem=questao_importada.importacao,
            prova_original=questao_importada.prova_original,
            numero_na_prova=questao_importada.numero_na_prova,
        )

    SimuladoQuestao.objects.update_or_create(
        simulado=questao_importada.importacao.simulado_original,
        questao=questao,
        defaults={
            'ordem': questao_importada.numero_na_prova,
            'peso': 1.00,
        },
    )

    QuestaoProvaOriginal.objects.update_or_create(
        questao=questao,
        prova_original=questao_importada.prova_original,
        defaults={
            'numero_na_prova': questao_importada.numero_na_prova,
            'importacao': questao_importada.importacao,
        },
    )

    questao_importada.questao_oficial = questao
    questao_importada.status = QuestaoImportada.PUBLICADA
    questao_importada.motivo_status = ''
    questao_importada.save(update_fields=['questao_oficial', 'status', 'motivo_status', 'atualizado_em'])

    atualizar_status_importacao(questao_importada.importacao)
    return questao


def atualizar_status_importacao(importacao):
    total = importacao.total_importadas
    publicadas = importacao.total_publicadas
    pendentes = importacao.total_pendentes
    correcao = importacao.total_correcao_necessaria

    if total == 0:
        importacao.status = ImportacaoProva.AGUARDANDO_REVISAO
        prova_status = ProvaOriginal.EM_REVISAO
    elif publicadas == 0:
        importacao.status = ImportacaoProva.AGUARDANDO_REVISAO
        prova_status = ProvaOriginal.EM_REVISAO
    elif publicadas == total:
        importacao.status = ImportacaoProva.PUBLICADA
        prova_status = ProvaOriginal.COMPLETA
    else:
        importacao.status = ImportacaoProva.PARCIALMENTE_PUBLICADA
        prova_status = (
            ProvaOriginal.EM_REVISAO if pendentes or correcao else ProvaOriginal.PARCIAL
        )

    importacao.save(update_fields=['status', 'atualizado_em'])
    if hasattr(importacao, 'prova_original'):
        importacao.prova_original.status_editorial = prova_status
        importacao.prova_original.save(update_fields=['status_editorial', 'atualizado_em'])
