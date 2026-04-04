from django.core.exceptions import ValidationError
from django.test import TestCase

from importador.models import ImportacaoProva, ProvaOriginal, QuestaoImportada
from importador.services import (
    classify_question,
    normalize_text,
    parse_gabarito,
    parse_question_block,
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
            {1: 'A', 2: 'B', 3: 'C', 10: 'E'},
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

    def test_split_question_blocks_accepts_broken_questao_marker(self):
        text = normalize_text(
            'QU EST ãO 60\nTexto da 60\nA opção A\nB opção B\n'
            'QU EST ãO 61\nTexto da 61\nA opção A\nB opção B'
        )
        blocks = split_question_blocks(text)
        self.assertIn(60, blocks)
        self.assertIn(61, blocks)

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
