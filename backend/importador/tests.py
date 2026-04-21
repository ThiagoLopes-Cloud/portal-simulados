import shutil
from pathlib import Path

from django.core.exceptions import ValidationError
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from conteudo.models import Materia, Tema
from importador.models import ImportacaoProva, ProvaOriginal, QuestaoImportada, QuestaoProvaOriginal
from importador.services import (
    build_public_media_url,
    build_public_media_urls_for_question,
    classify_question,
    clean_extracted_field,
    normalize_text,
    parse_gabarito,
    parse_question_block,
    publicar_questao_importada,
    select_owner_block_for_page,
    split_question_blocks,
    question_has_visual_hint,
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

    def test_classify_question_requires_image_when_visual_hint_exists(self):
        status, reason = classify_question(
            {
                'texto_bruto': 'Observe a figura e responda.',
                'enunciado': 'Observe a figura e responda.',
                'opcao_a': 'A',
                'opcao_b': 'B',
                'opcao_c': 'C',
                'opcao_d': 'D',
                'opcao_e': 'E',
            },
            'A',
            has_image=False,
        )
        self.assertEqual(status, QuestaoImportada.CORRECAO_NECESSARIA)
        self.assertIn('indicativo visual', reason)

    def test_question_has_visual_hint_detects_chart_and_figure_terms(self):
        self.assertTrue(question_has_visual_hint('Observe o grafico e assinale a alternativa correta.'))
        self.assertTrue(question_has_visual_hint('A figura a seguir apresenta um mapa.'))
        self.assertTrue(question_has_visual_hint('Nesse cartaz publicitario, os recursos verbais e nao verbais...'))
        self.assertFalse(question_has_visual_hint('Texto puramente conceitual sem apoio visual.'))

    def test_select_owner_block_for_page_prefers_unique_visual_block(self):
        blocks = [
            {
                'numero': 11,
                'texto': 'Texto da questao.\nA figura decorativa da mulher ante o protagonismo masculino.',
                'pagina_inicial': 8,
                'paginas': [8],
            },
            {
                'numero': 14,
                'texto': 'Disponivel em exemplo.\nNesse cartaz publicitario, os recursos verbais e nao verbais...',
                'pagina_inicial': 8,
                'paginas': [8, 9],
            },
        ]
        owner = select_owner_block_for_page(8, blocks)
        self.assertEqual(owner['numero'], 14)

    def test_select_owner_block_for_page_without_visual_hint_uses_last_starting_block(self):
        blocks = [
            {'numero': 3, 'texto': 'Texto da 3', 'pagina_inicial': 3, 'paginas': [2, 3]},
            {'numero': 4, 'texto': 'Texto da 4', 'pagina_inicial': 3, 'paginas': [3]},
            {'numero': 5, 'texto': 'Texto da 5', 'pagina_inicial': 3, 'paginas': [3, 4]},
        ]
        owner = select_owner_block_for_page(3, blocks)
        self.assertEqual(owner['numero'], 5)


class ImportacaoDeleteBehaviorTests(TestCase):
    def test_can_delete_importacao_even_when_simulado_has_results(self):
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

        importacao.delete()

        self.assertFalse(ImportacaoProva.objects.filter(pk=importacao.pk).exists())
        self.assertFalse(Simulado.objects.filter(pk=simulado.pk).exists())


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


class TemaEDificuldadeImportadasTests(TestCase):
    def test_questao_importada_nasce_com_dificuldade_media_por_padrao(self):
        user = User.objects.create_user(username='admin4', password='senha123', role='admin')
        importacao = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova2025.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2025.pdf',
            criado_por=user,
        )
        prova = ProvaOriginal.objects.create(importacao=importacao, descricao='ENEM 2025 - Azul')

        questao = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=12,
            enunciado='Enunciado importado.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='A',
        )

        self.assertEqual(questao.dificuldade, 'M')
        self.assertIsNone(questao.tema)

    def test_publicacao_propaga_tema_e_dificuldade_para_questao_oficial(self):
        user = User.objects.create_user(username='admin5', password='senha123', role='admin')
        materia = Materia.objects.create(nome='Fisica', codigo='FIS')
        tema = Tema.objects.create(nome='Mecanica', materia=materia)

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

        importada = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=25,
            tema=tema,
            dificuldade='D',
            enunciado='Enunciado com tema e dificuldade.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='B',
        )

        questao = publicar_questao_importada(importada)

        self.assertEqual(questao.tema, tema)
        self.assertEqual(questao.dificuldade, 'D')


class ImagemEnunciadoImportadaTests(TestCase):
    def setUp(self):
        self.temp_media = Path(settings.BASE_DIR) / 'test_media_importador'
        self.temp_media.mkdir(parents=True, exist_ok=True)
        self.override = override_settings(
            MEDIA_ROOT=str(self.temp_media),
            MEDIA_URL='/media/',
            PUBLIC_BASE_URL='http://testserver',
        )
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.temp_media, ignore_errors=True)

    def test_build_public_media_url_uses_public_base_url(self):
        user = User.objects.create_user(username='admin7', password='senha123', role='admin')
        importacao = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova2025.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2025.pdf',
            criado_por=user,
        )
        prova = ProvaOriginal.objects.create(importacao=importacao, descricao='ENEM 2025 - Azul')
        questao = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=8,
            enunciado='Questao com imagem.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='A',
        )
        questao.imagem_enunciado_arquivo.save(
            'teste.png',
            SimpleUploadedFile('teste.png', b'fake-image', content_type='image/png'),
            save=True,
        )

        self.assertEqual(
            build_public_media_url(questao.imagem_enunciado_arquivo),
            f'http://testserver{questao.imagem_enunciado_arquivo.url}',
        )

    def test_build_public_media_urls_for_question_includes_alternative_images(self):
        user = User.objects.create_user(username='admin7b', password='senha123', role='admin')
        importacao = ImportacaoProva.objects.create(
            ano=2025,
            dia=1,
            cor=ImportacaoProva.COR_AZUL,
            pdf_prova='importacoes/provas/prova2025.pdf',
            pdf_gabarito='importacoes/gabaritos/gabarito2025.pdf',
            criado_por=user,
        )
        prova = ProvaOriginal.objects.create(importacao=importacao, descricao='ENEM 2025 - Azul')
        questao = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=9,
            enunciado='Questao com imagens nas alternativas.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='A',
        )
        questao.imagem_opcao_a_arquivo.save(
            'alt_a.png',
            SimpleUploadedFile('alt_a.png', b'fake-image-a', content_type='image/png'),
            save=True,
        )
        questao.imagem_opcao_c_arquivo.save(
            'alt_c.png',
            SimpleUploadedFile('alt_c.png', b'fake-image-c', content_type='image/png'),
            save=True,
        )

        urls = build_public_media_urls_for_question(questao)

        self.assertEqual(urls['imagem_opcao_a'], f'http://testserver{questao.imagem_opcao_a_arquivo.url}')
        self.assertIsNone(urls['imagem_opcao_b'])
        self.assertEqual(urls['imagem_opcao_c'], f'http://testserver{questao.imagem_opcao_c_arquivo.url}')

    def test_publicacao_propaga_imagem_enunciado_para_questao_oficial(self):
        user = User.objects.create_user(username='admin8', password='senha123', role='admin')
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
        importada = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=18,
            enunciado='Questao com imagem publicada.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='B',
        )
        importada.imagem_enunciado_arquivo.save(
            'figura.png',
            SimpleUploadedFile('figura.png', b'fake-image', content_type='image/png'),
            save=True,
        )

        questao = publicar_questao_importada(importada)

        self.assertEqual(
            questao.imagem_enunciado,
            f'http://testserver{importada.imagem_enunciado_arquivo.url}',
        )

    def test_publicacao_propaga_imagens_das_alternativas_para_questao_oficial(self):
        user = User.objects.create_user(username='admin8b', password='senha123', role='admin')
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
        importada = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=19,
            enunciado='Questao com imagens nas alternativas publicadas.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='B',
        )
        importada.imagem_opcao_a_arquivo.save(
            'alt_a.png',
            SimpleUploadedFile('alt_a.png', b'fake-image-a', content_type='image/png'),
            save=True,
        )
        importada.imagem_opcao_d_arquivo.save(
            'alt_d.png',
            SimpleUploadedFile('alt_d.png', b'fake-image-d', content_type='image/png'),
            save=True,
        )

        questao = publicar_questao_importada(importada)

        self.assertEqual(
            questao.imagem_opcao_a,
            f'http://testserver{importada.imagem_opcao_a_arquivo.url}',
        )
        self.assertIsNone(questao.imagem_opcao_b)
        self.assertEqual(
            questao.imagem_opcao_d,
            f'http://testserver{importada.imagem_opcao_d_arquivo.url}',
        )

    def test_dedupe_reaproveita_questao_e_completa_tema_ausente(self):
        user = User.objects.create_user(username='admin6', password='senha123', role='admin')
        materia = Materia.objects.create(nome='Fisica', codigo='FIS')
        tema = Tema.objects.create(nome='Termologia', materia=materia)

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

        Questao.objects.create(
            enunciado='Mesmo enunciado.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            resposta_correta='C',
            dificuldade='M',
            explicacao='',
            fonte='ENEM oficial - INEP',
            ano_origem=2025,
            revisado=True,
        )

        importada = QuestaoImportada.objects.create(
            importacao=importacao,
            prova_original=prova,
            numero_na_prova=42,
            tema=tema,
            dificuldade='D',
            enunciado='Mesmo enunciado.',
            opcao_a='A',
            opcao_b='B',
            opcao_c='C',
            opcao_d='D',
            opcao_e='E',
            gabarito_oficial='C',
        )

        questao = publicar_questao_importada(importada)

        self.assertEqual(questao.tema, tema)
        self.assertEqual(questao.dificuldade, 'D')
