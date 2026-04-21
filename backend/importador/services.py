import os
import re
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
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
QUESTION_RANGE_RE = re.compile(r'Quest[õo]es de \d+ a \d+', re.IGNORECASE)
GABARITO_BILINGUAL_HEADER_RE = re.compile(r'INGL[ÊE]S\s+ESPANHOL', re.IGNORECASE)
VISUAL_HINT_RE = re.compile(
    r'\b(figura|imagem|grafico|gr[aá]fico|tabela|mapa|charge|cartum|tirinha|quadrinho|'
    r'infografico|infogr[aá]fico|esquema|ilustracao|ilustra[cç][aã]o|fotografia|foto)\b',
    re.IGNORECASE,
)


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


def guess_image_extension(image_name, image_data):
    extension = Path(image_name).suffix.lower()
    if extension in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.jp2'}:
        return extension

    signatures = [
        (b'\x89PNG\r\n\x1a\n', '.png'),
        (b'\xff\xd8\xff', '.jpg'),
        (b'GIF87a', '.gif'),
        (b'GIF89a', '.gif'),
        (b'BM', '.bmp'),
        (b'II*\x00', '.tif'),
        (b'MM\x00*', '.tif'),
        (b'\x00\x00\x00\x0cjP  \r\n\x87\n', '.jp2'),
    ]
    for signature, guessed_extension in signatures:
        if image_data.startswith(signature):
            return guessed_extension
    return '.bin'


def extract_pdf_pages(file_field):
    file_field.open('rb')
    try:
        reader = PdfReader(file_field)
        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            images = []
            for image_index, image in enumerate(getattr(page, 'images', []), start=1):
                data = getattr(image, 'data', None)
                if not data:
                    continue
                original_name = getattr(image, 'name', f'page_{page_number}_image_{image_index}')
                images.append(
                    {
                        'page_number': page_number,
                        'name': original_name,
                        'data': data,
                        'extension': guess_image_extension(original_name, data),
                    }
                )
            pages.append(
                {
                    'number': page_number,
                    'text': normalize_text(page.extract_text() or ''),
                    'images': images,
                }
            )
    finally:
        file_field.close()
    return pages


def extract_pdf_text(file_field):
    return '\n'.join(page['text'] for page in extract_pdf_pages(file_field))


def parse_gabarito(text):
    answers = OrderedDict()
    flat_matches = re.findall(r'(\d{1,3})\s+([A-E])(?:\s+([A-E]))?', text)
    if flat_matches and '\n' not in text:
        for numero, primeira, segunda in flat_matches:
            numero_int = int(numero)
            if segunda and numero_int <= 5:
                answers[(numero_int, QuestaoImportada.IDIOMA_INGLES)] = primeira
                answers[(numero_int, QuestaoImportada.IDIOMA_ESPANHOL)] = segunda
            else:
                answers[(numero_int, None)] = primeira
        return answers

    bilingual_mode = False

    for raw_line in text.splitlines():
        line = re.sub(r'\s+', ' ', raw_line).strip()
        if not line:
            continue
        if GABARITO_BILINGUAL_HEADER_RE.search(line):
            bilingual_mode = True
            continue

        parts = line.split()
        if not parts or not parts[0].isdigit():
            continue

        numero_int = int(parts[0])
        if not 1 <= numero_int <= 200:
            continue

        alternativas = [token.upper() for token in parts[1:] if token.upper() in {'A', 'B', 'C', 'D', 'E'}]
        if not alternativas:
            continue

        if bilingual_mode and numero_int <= 5 and len(alternativas) >= 2:
            answers[(numero_int, QuestaoImportada.IDIOMA_INGLES)] = alternativas[0]
            answers[(numero_int, QuestaoImportada.IDIOMA_ESPANHOL)] = alternativas[1]
        else:
            answers[(numero_int, None)] = alternativas[0]
    return answers


def detect_language_section(line):
    normalized = line.lower()
    if '01 a 05' not in normalized:
        return None
    if 'ingl' in normalized:
        return QuestaoImportada.IDIOMA_INGLES
    if 'espanhol' in normalized:
        return QuestaoImportada.IDIOMA_ESPANHOL
    return None


def split_question_blocks(text):
    return split_question_blocks_from_pages(
        [{'number': 1, 'text': text, 'images': []}]
    )


def split_question_blocks_from_pages(page_entries):
    blocks = []
    current_number = None
    current_language = None
    current_lines = []
    current_pages = []

    def flush_current():
        nonlocal current_number, current_language, current_lines, current_pages
        if current_number is None or not current_lines:
            return
        blocks.append(
            {
                'numero': current_number,
                'idioma': current_language if current_number <= 5 else None,
                'texto': '\n'.join(current_lines).strip(),
                'pagina_inicial': current_pages[0] if current_pages else None,
                'paginas': current_pages[:],
            }
        )
        current_number = None
        current_lines = []
        current_pages = []

    for page_entry in page_entries:
        page_number = page_entry['number']
        if current_number is not None and page_number not in current_pages:
            current_pages.append(page_number)

        for line in page_entry['text'].splitlines():
            language = detect_language_section(line)
            if language:
                flush_current()
                current_language = language
                continue

            if QUESTION_RANGE_RE.search(line) and current_number is None and current_language and '01 a 05' not in line:
                current_language = None

            match = QUESTION_LINE_RE.search(line)
            if match:
                number = int(match.group(1))
                if 1 <= number <= 200:
                    flush_current()
                    current_number = number
                    if number > 5:
                        current_language = None
                    current_lines = []
                    current_pages = [page_number]
                    continue

            if current_number is not None:
                current_lines.append(line)

    flush_current()
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

    return {
        'texto_bruto': block_text.strip(),
        'enunciado': clean_extracted_field('\n'.join(enunciado_lines)),
        'opcao_a': clean_extracted_field('\n'.join(alternatives['A'])),
        'opcao_b': clean_extracted_field('\n'.join(alternatives['B'])),
        'opcao_c': clean_extracted_field('\n'.join(alternatives['C'])),
        'opcao_d': clean_extracted_field('\n'.join(alternatives['D'])),
        'opcao_e': clean_extracted_field('\n'.join(alternatives['E'])),
    }


def question_has_visual_hint(text):
    return bool(VISUAL_HINT_RE.search(text or ''))


def classify_question(parsed, answer, has_image=False):
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

    if question_has_visual_hint(parsed.get('texto_bruto', parsed.get('enunciado', ''))) and not has_image:
        problems.append('Questao com indicativo visual sem imagem associada.')

    status = (
        QuestaoImportada.CORRECAO_NECESSARIA if problems
        else QuestaoImportada.PENDENTE_APROVACAO
    )
    return status, ' '.join(problems)


def infer_expected_total(question_blocks, gabarito):
    return max(
        max((item['numero'] for item in question_blocks), default=0),
        max((numero for numero, _idioma in gabarito.keys()), default=0),
    )


def canonicalize_question_text(text):
    cleaned = clean_extracted_field(text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return cleaned


def find_existing_question(questao_importada):
    candidatos = Questao.objects.filter(
        resposta_correta=questao_importada.gabarito_oficial,
        idioma=questao_importada.idioma,
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


def build_public_media_url(file_field):
    if not file_field or not getattr(file_field, 'name', None):
        return None

    base_url = (
        getattr(settings, 'PUBLIC_BASE_URL', '')
        or os.getenv('PUBLIC_BASE_URL')
        or os.getenv('BACKEND_PUBLIC_URL')
        or 'http://localhost:8000'
    ).rstrip('/')
    return urljoin(f'{base_url}/', file_field.url.lstrip('/'))


def question_blocks_overlap(block_a, block_b):
    return bool(set(block_a.get('paginas', [])) & set(block_b.get('paginas', [])))


def select_image_for_block(block, all_blocks, page_entries_by_number):
    page_numbers = block.get('paginas') or ([block['pagina_inicial']] if block.get('pagina_inicial') else [])
    candidate_images = []
    competing_blocks = []

    for other_block in all_blocks:
        if question_blocks_overlap(block, other_block):
            competing_blocks.append(other_block)

    for page_number in page_numbers:
        page_entry = page_entries_by_number.get(page_number)
        if page_entry:
            candidate_images.extend(page_entry['images'])

    if not candidate_images:
        return None, None

    if len(candidate_images) == 1:
        image = candidate_images[0]
        if len(competing_blocks) == 1:
            return image, None

        visual_blocks = [item for item in competing_blocks if question_has_visual_hint(item['texto'])]
        if len(visual_blocks) == 1 and visual_blocks[0] is block:
            return image, None

        return None, 'Imagem presente na pagina, mas associacao esta ambigua.'

    if len(competing_blocks) == 1:
        return candidate_images[0], 'Multiplas imagens detectadas; a primeira foi associada para revisao.'

    return None, 'Multiplas imagens detectadas na mesma area da prova.'


def save_extracted_image(questao_importada, image_info):
    suffix = image_info['extension'] if image_info['extension'].startswith('.') else f".{image_info['extension']}"
    idioma_suffix = questao_importada.idioma or 'geral'
    filename = (
        f"enem_{questao_importada.importacao.ano}_d{questao_importada.importacao.dia}_"
        f"{questao_importada.importacao.cor}_q{questao_importada.numero_na_prova}_{idioma_suffix}_"
        f"p{questao_importada.pagina_inicial or image_info['page_number']}{suffix}"
    )
    questao_importada.imagem_enunciado_arquivo.save(
        filename,
        ContentFile(image_info['data']),
        save=False,
    )


@transaction.atomic
def processar_importacao(importacao):
    importacao.status = ImportacaoProva.PROCESSANDO
    importacao.mensagem_erro = ''
    importacao.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])

    if not importacao.pdf_prova or not importacao.pdf_gabarito:
        raise ValidationError('Envie os PDFs da prova e do gabarito.')

    prova_pages = extract_pdf_pages(importacao.pdf_prova)
    prova_texto = '\n'.join(page['text'] for page in prova_pages)
    gabarito_texto = extract_pdf_text(importacao.pdf_gabarito)

    question_blocks = split_question_blocks_from_pages(prova_pages)
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

    max_gabarito = max((numero for numero, _idioma in gabarito.keys()), default=0)
    if max_gabarito:
        question_blocks = [
            item for item in question_blocks
            if item['numero'] <= max_gabarito
        ]

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

    page_entries_by_number = {page['number']: page for page in prova_pages}
    created = []
    for item in question_blocks:
        numero = item['numero']
        idioma = item['idioma']
        parsed = parse_question_block(item['texto'])
        answer = gabarito.get((numero, idioma), '')
        if not answer and idioma is not None:
            answer = gabarito.get((numero, None), '')

        image_info, image_reason = select_image_for_block(item, question_blocks, page_entries_by_number)
        status, reason = classify_question(parsed, answer, has_image=bool(image_info))
        if image_reason:
            reason = f'{reason} {image_reason}'.strip()

        questao_importada = QuestaoImportada(
            importacao=importacao,
            prova_original=prova_original,
            numero_na_prova=numero,
            pagina_inicial=item.get('pagina_inicial'),
            idioma=idioma,
            texto_bruto=parsed['texto_bruto'],
            enunciado=parsed['enunciado'],
            opcao_a=parsed['opcao_a'],
            opcao_b=parsed['opcao_b'],
            opcao_c=parsed['opcao_c'],
            opcao_d=parsed['opcao_d'],
            opcao_e=parsed['opcao_e'],
            dificuldade='M',
            gabarito_oficial=answer,
            status=status,
            motivo_status=reason,
        )
        if image_info:
            save_extracted_image(questao_importada, image_info)
        questao_importada.save()
        created.append(questao_importada)

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

    imagem_enunciado_url = build_public_media_url(questao_importada.imagem_enunciado_arquivo)

    questao = find_existing_question(questao_importada)
    if questao is None:
        questao = Questao.objects.create(
            enunciado=questao_importada.enunciado,
            tema=questao_importada.tema,
            imagem_enunciado=imagem_enunciado_url,
            opcao_a=questao_importada.opcao_a,
            opcao_b=questao_importada.opcao_b,
            opcao_c=questao_importada.opcao_c,
            opcao_d=questao_importada.opcao_d,
            opcao_e=questao_importada.opcao_e,
            resposta_correta=questao_importada.gabarito_oficial,
            dificuldade=questao_importada.dificuldade,
            explicacao='',
            fonte='ENEM oficial - INEP',
            ano_origem=questao_importada.importacao.ano,
            idioma=questao_importada.idioma,
            revisado=True,
            importacao_origem=questao_importada.importacao,
            prova_original=questao_importada.prova_original,
            numero_na_prova=questao_importada.numero_na_prova,
        )
    else:
        updated_fields = []
        if questao.tema_id is None and questao_importada.tema_id is not None:
            questao.tema = questao_importada.tema
            updated_fields.append('tema')
        if (
            questao.dificuldade == 'M'
            and questao_importada.dificuldade in {'F', 'D'}
        ):
            questao.dificuldade = questao_importada.dificuldade
            updated_fields.append('dificuldade')
        if not questao.imagem_enunciado and imagem_enunciado_url:
            questao.imagem_enunciado = imagem_enunciado_url
            updated_fields.append('imagem_enunciado')
        if updated_fields:
            questao.save(update_fields=updated_fields + ['atualizado_em'])

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
        idioma=questao_importada.idioma,
        defaults={
            'numero_na_prova': questao_importada.numero_na_prova,
            'idioma': questao_importada.idioma,
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
