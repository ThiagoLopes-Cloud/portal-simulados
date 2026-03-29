# questoes/models.py
# Model de Questao desacoplado de qualquer simulado específico.
# Uma questão agora é um recurso reutilizável do banco de questões,
# podendo aparecer em múltiplos simulados via SimuladoQuestao.

from django.db import models
from conteudo.models import Tema


class Questao(models.Model):
    """
    Representa uma questão de múltipla escolha do banco de questões.
    Desacoplada do Simulado — o vínculo agora ocorre via SimuladoQuestao.
    Suporta o formato ENEM com 5 alternativas (A–E).
    """

    OPCAO_A = 'A'
    OPCAO_B = 'B'
    OPCAO_C = 'C'
    OPCAO_D = 'D'
    OPCAO_E = 'E'

    OPCOES_CHOICES = [
        (OPCAO_A, 'Alternativa A'),
        (OPCAO_B, 'Alternativa B'),
        (OPCAO_C, 'Alternativa C'),
        (OPCAO_D, 'Alternativa D'),
        (OPCAO_E, 'Alternativa E'),
    ]

    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]

    # Tema ao qual a questão pertence — usado para diagnóstico de desempenho
    tema = models.ForeignKey(
        Tema,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questoes',
        verbose_name='Tema'
    )

    # Enunciado principal da questão
    enunciado = models.TextField(verbose_name='Enunciado')

    # URL de imagem opcional para ilustrar o enunciado
    imagem_enunciado = models.URLField(
        blank=True,
        null=True,
        verbose_name='Imagem do Enunciado (URL)',
        help_text='Cole a URL de uma imagem para ilustrar o enunciado (opcional)'
    )

    # Alternativas de A a E — E é opcional (questões de 4 alternativas deixam vazio)
    opcao_a = models.CharField(max_length=500, verbose_name='Alternativa A')
    opcao_b = models.CharField(max_length=500, verbose_name='Alternativa B')
    opcao_c = models.CharField(max_length=500, verbose_name='Alternativa C')
    opcao_d = models.CharField(max_length=500, verbose_name='Alternativa D')
    opcao_e = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Alternativa E'
    )

    # URLs de imagens opcionais para cada alternativa
    imagem_opcao_a = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa A (URL)')
    imagem_opcao_b = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa B (URL)')
    imagem_opcao_c = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa C (URL)')
    imagem_opcao_d = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa D (URL)')
    imagem_opcao_e = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa E (URL)')

    # Gabarito — qual alternativa é a correta
    resposta_correta = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Resposta Correta'
    )

    # Nível de dificuldade — usado para análise de desempenho e recomendação
    dificuldade = models.CharField(
        max_length=1,
        choices=DIFICULDADE_CHOICES,
        default='M',
        verbose_name='Dificuldade'
    )

    # Explicação do gabarito — exibida após o aluno responder
    explicacao = models.TextField(
        blank=True,
        verbose_name='Explicação do gabarito'
    )

    # Ano de origem da questão (ex: ENEM 2023) — útil para filtros futuros
    ano_origem = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Ano de Origem'
    )

    # Identificador único de origem para importações via API (impede duplicatas)
    id_origem = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name='ID de Origem'
    )

    # Fonte da questão (ex: "ENEM 2023 — Caderno Amarelo")
    fonte = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Fonte'
    )

    # Timestamps automáticos
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        tema_nome = self.tema.nome if self.tema else 'Sem tema'
        return f'[{self.get_dificuldade_display()}] {tema_nome} — {self.enunciado[:60]}...'

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['-criado_em']