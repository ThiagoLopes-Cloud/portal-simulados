from django.core.exceptions import ValidationError
from django.test import TestCase

from importador.models import ImportacaoProva, ProvaOriginal, QuestaoImportada, QuestaoProvaOriginal
from importador.services import (
    classify_question,
    clean_extracted_field,
    normalize_text,
    parse_gabarito,
    parse_question_block,
    publicar_questao_importada,
    split_question_blocks,
)
from questoes.models import Questao
from simulados.models import Simulado
from users.models import User


class ImportadorParsingTests(TestCase):
    def test_parse_gabarito_extracts_pairs(self):
        text = '1 A 2 B 3 C 10 E'
        self.assertEqual(
            parse_gabarito(text),
            {(1, None): 'A', (2, None): 'B', (3, None): 'C', (10, None): 'E'},
        )

    def test_parse_gabarito_extracts_ingles_e_espanhol(self):
        text = (
            'QUESTAO GABARITO INGLES ESPANHOL\n'
            '1 D B\n'
            '2 D A\n'
            '5 A C\n'
            '6 E'
        )
        self.assertEqual(
            parse_gabarito(text),
            {
                (1, QuestaoImportada.IDIOMA_INGLES): 'D',
                (1, QuestaoImportada.IDIOMA_ESPANHOL): 'B',
                (2, QuestaoImportada.IDIOMA_INGLES): 'D',
                (2, QuestaoImportada.IDIOMA_ESPANHOL): 'A',
                (5, QuestaoImportada.IDIOMA_INGLES): 'A',
                (5, QuestaoImportada.IDIOMA_ESPANHOL): 'C',
                (6, None): 'E',
            },
        )

    def test_parse_question_block_splits_enunciado_and_alternatives(self):
        parsed = parse_question_block(
            'Texto base da questão\nA) Alternativa A\nB) Alternativa B\n'
            'C) Alternativa C\nD) Alternativa D\nE) Alternativa E'
        )
        self.assertEqual(parsed['enunciado'], 'Texto base da questão')
        self.assertEqual(parsed['opcao_a'], 'Alternativa A')
        self.assertEqual(parsed['opcao_e'], 'Alternativa E')

    def test_parse_question_block_accepts_alternative_with_space_after_letter(self):
        parsed = parse_question_block(
            'Enunciado de teste\nA alternativa A\nB alternativa B\n'
            'C alternativa C\nD alternativa D\nE alternativa E'
        )
        self.assertEqual(parsed['opcao_a'], 'alternativa A')
        self.assertEqual(parsed['opcao_d'], 'alternativa D')

    def test_parse_question_block_keeps_enunciado_that_starts_with_a(self):
        parsed = parse_question_block(
            'A atmosfera terrestre contém gases importantes.\n'
            'Considerando o texto, a alternativa correta é\n'
            'A reduzir emissões.\n'
            'B aumentar consumo.\n'
            'C manter tudo igual.\n'
            'D ignorar o problema.\n'
            'E retirar vapor d água.'
        )
        self.assertTrue(parsed['enunciado'].startswith('A atmosfera terrestre'))
        self.assertEqual(parsed['opcao_a'], 'reduzir emissões.')

    def test_clean_extracted_field_joins_word_broken_across_lines(self):
        cleaned = clean_extracted_field('cri\nar a moeda propria.')
        self.assertEqual(cleaned, 'criar a moeda propria.')

    def test_clean_extracted_field_removes_pdf_header_noise(self):
        cleaned = clean_extracted_field(
            'des\nigualdade de genero acentuada pela baixa escolarizacao.\n'
            'LINGUAGENS, CODIGOS E SUAS TECNOLOGIAS E REDACAO | 1o DIA | CADERNO 1 | AZUL18'
        )
        self.assertEqual(
            cleaned,
            'desigualdade de genero acentuada pela baixa escolarizacao.'
        )

    def test_clean_extracted_field_joins_broken_suffix_from_previous_line(self):
        cleaned = clean_extracted_field('aura de mis\ntério sobre a identidade da jovem.')
        self.assertEqual(cleaned, 'aura de mistério sobre a identidade da jovem.')

    def test_clean_extracted_field_stops_at_next_section_intro(self):
        cleaned = clean_extracted_field(
            'indiferenca em relacao a fatos historicos.\n'
            'Texto para as QUESTAO 06 a 10.\n'
            'De proprio punho'
        )
        self.assertEqual(cleaned, 'indiferenca em relacao a fatos historicos.')

    def test_clean_extracted_field_stops_at_redacao_intro(self):
        cleaned = clean_extracted_field(
            'apontar para a dificuldade de compreensao do termo.\n'
            'PROPOSTA DE REDACAO\n'
            'A partir da leitura dos textos motivadores'
        )
        self.assertEqual(cleaned, 'apontar para a dificuldade de compreensao do termo.')

    def test_split_question_blocks_accepts_broken_questao_marker(self):
        text = normalize_text(
            'QU EST ãO 60\nTexto da 60\nA opção A\nB opção B\n'
            'QU EST ãO 61\nTexto da 61\nA opção A\nB opção B'
        )
        blocks = split_question_blocks(text)
        self.assertEqual(
            [item['numero'] for item in blocks],
            [60, 61],
        )

    def test_split_question_blocks_tracks_bilingual_language_sections(self):
        text = normalize_text(
            'Questoes de 01 a 05 (opcao ingles)\n'
            'QUESTAO 01\nTexto ingles\nA alt A\nB alt B\nC alt C\nD alt D\nE alt E\n'
            'Questoes de 01 a 05 (opcao espanhol)\n'
            'QUESTAO 01\nTexto espanhol\nA alt A\nB alt B\nC alt C\nD alt D\nE alt E\n'
            'QUESTAO 06\nTexto geral\nA alt A\nB alt B\nC alt C\nD alt D\nE alt E'
        )
        blocks = split_question_blocks(text)
        self.assertEqual(
            [(item['numero'], item['idioma']) for item in blocks[:3]],
            [
                (1, QuestaoImportada.IDIOMA_INGLES),
                (1, QuestaoImportada.IDIOMA_ESPANHOL),
                (6, None),
            ],
        )

    def test_normalize_text_removes_known_pdf_noise(self):
        text = normalize_text(
            '*010175AZ32*\nENEM2025ENEM2025\n010175AZ.indb 32\n'
            'CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS | 1º DIA | CADERNO 1 | AZUL26\n'
            'QUESTAO 10\nTexto útil'
        )
        self.assertNotIn('ENEM2025', text)
        self.assertNotIn('.indb', text)
        self.assertIn('QUESTAO 10', text)

    def test_classify_question_marks_broken_content_for_review(self):
        status, reason = classify_question(
            {
                'enunciado': 'Questão incompleta',
                'opcao_a': 'A',
                'opcao_b': 'B',
                'opcao_c': '',
                'opcao_d': 'D',
                'opcao_e': 'E',
            },
            'A',
        )
        self.assertEqual(status, QuestaoImportada.CORRECAO_NECESSARIA)
        self.assertIn('Alternativas ausentes', reason)


class ImportacaoDeleteProtectionTests(TestCase):
    def test_cannot_delete_importacao_when_simulado_has_results(self):
        user = User.objects.create_user(
            username='admin',
            password='senha123',
            role='admin',
        )
        importacao = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito.pdf',
            criado_por=user,
        )
        prova = ProvaOriginal.objects.create(importacao=importacao, descricao='ENEM 2025')
        simulado = Simulado.objects.create(
            titulo='ENEM 2025 - Dia 1 - Azul',
            descricao='Original',
            criado_por=user,
            ativo=False,
            importacao_origem=importacao,
            prova_original=prova,
            eh_simulado_original=True,
        )
        Questao.objects.create(
            enunciado='Questão teste',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            resposta_correta='A',
            importacao_origem=importacao,
            prova_original=prova,
            numero_na_prova=1,
            revisado=True,
        )
        simulado.resultados.create(aluno=user, tentativa=1, acertos=1, total_questoes=1, score=100)

        with self.assertRaises(ValidationError):
            importacao.delete()


class DedupeQuestaoEntreProvasTests(TestCase):
    def test_publicacao_reaproveita_questao_existente_em_outra_prova(self):
        user = User.objects.create_user(username='admin2', password='senha123', role='admin')

        importacao_2009 = ImportacaoProva.objects.create(
            ano=2009,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova2009.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2009.pdf',
            criado_por=user,
        )
        prova_2009 = ProvaOriginal.objects.create(importacao=importacao_2009, descricao='ENEM 2009 - Azul')
        Simulado.objects.create(
            titulo='ENEM 2009 - Dia 1 - Azul',
            descricao='Original',
            criado_por=user,
            ativo=False,
            importacao_origem=importacao_2009,
            prova_original=prova_2009,
            eh_simulado_original=True,
        )
        importada_2009 = QuestaoImportada.objects.create(
            importacao=importacao_2009,
            prova_original=prova_2009,
            numero_na_prova=1,
            enunciado='Enunciado igual nas duas provas.',
            opcao_a='Alternativa A',
            opcao_b='Alternativa B',
            opcao_c='Alternativa C',
            opcao_d='Alternativa D',
            opcao_e='Alternativa E',
            gabarito_oficial='A',
        )

        questao_base = publicar_questao_importada(importada_2009)

        importacao_2025 = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_BRANCO,
            pdf_prova='importacoes/provas/prova2025.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2025.pdf',
            criado_por=user,
        )
        prova_2025 = ProvaOriginal.objects.create(importacao=importacao_2025, descricao='ENEM 2025 - Branco')
        Simulado.objects.create(
            titulo='ENEM 2025 - Dia 1 - Branco',
            descricao='Original',
            criado_por=user,
            ativo=False,
            importacao_origem=importacao_2025,
            prova_original=prova_2025,
            eh_simulado_original=True,
        )
        importada_2025 = QuestaoImportada.objects.create(
            importacao=importacao_2025,
            prova_original=prova_2025,
            numero_na_prova=77,
            enunciado='Enunciado igual nas duas provas.',
            opcao_a='Alternativa A',
            opcao_b='Alternativa B',
            opcao_c='Alternativa C',
            opcao_d='Alternativa D',
            opcao_e='Alternativa E',
            gabarito_oficial='A',
        )

        questao_reutilizada = publicar_questao_importada(importada_2025)

        self.assertEqual(questao_base.id, questao_reutilizada.id)
        self.assertEqual(Questao.objects.count(), 1)
        self.assertEqual(
            QuestaoProvaOriginal.objects.filter(questao=questao_base).count(),
            2,
        )
        provas = list(
            QuestaoProvaOriginal.objects.filter(questao=questao_base)
            .values_list('prova_original__importacao__ano', 'prova_original__importacao__cor', 'numero_na_prova')
            .order_by('prova_original__importacao__ano')
        )
        self.assertEqual(
            provas,
            [(2009, ImportacaoProva.COR_AZUL, 1), (2025, ImportacaoProva.COR_BRANCO, 77)],
        )

    def test_publicacao_nao_reaproveita_questao_quando_idioma_e_diferente(self):
        user = User.objects.create_user(username='admin3', password='senha123', role='admin')

        importacao = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova2025.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2025.pdf',
            criado_por=user,
        )
        prova = ProvaOriginal.objects.create(importacao=importacao, descricao='ENEM 2025 - Azul')
        Simulado.objects.create(
            titulo='ENEM 2025 - Dia 1 - Azul',
            descricao='Original',
            criado_por=user,
            ativo=False,
            importacao_origem=importacao,
            prova_original=prova,
            eh_simulado_original=True,
        )

        ingles = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=1,
            idioma=QuestaoImportada.IDIOMA_INGLES,
            enunciado='Texto equivalente.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='A',
        )
        espanhol = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=1,
            idioma=QuestaoImportada.IDIOMA_ESPANHOL,
            enunciado='Texto equivalente.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='A',
        )

        q_ingles = publicar_questao_importada(ingles)
        q_espanhol = publicar_questao_importada(espanhol)

        self.assertNotEqual(q_ingles.id, q_espanhol.id)
        self.assertEqual(Questao.objects.filter(enunciado='Texto equivalente.').count(), 2)
