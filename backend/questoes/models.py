from django.db import models
from conteudo.models import Tema

class Questao(models.Model):
    """
    Representa uma questão de múltipla escolha vinculada a um simulado.
    Adaptada para o formato ENEM com 5 alternativas (A, B, C, D, E).
    """

    # Opções de resposta disponíveis — 5 alternativas padrão ENEM
    OPCAO_A = 'A'
    OPCAO_B = 'B'
    OPCAO_C = 'C'
    OPCAO_D = 'D'
    OPCAO_E = 'E'  # ← nova opção

    OPCOES_CHOICES = [
        (OPCAO_A, 'Alternativa A'),
        (OPCAO_B, 'Alternativa B'),
        (OPCAO_C, 'Alternativa C'),
        (OPCAO_D, 'Alternativa D'),
        (OPCAO_E, 'Alternativa E'),  # ← nova opção
    ]

    # ForeignKey com o simulado
    simulado = models.ForeignKey(
        'simulados.Simulado',
        on_delete=models.CASCADE,
        related_name='questoes',
        verbose_name='Simulado'
    )

    # NOVO — Relacionamento com o tema da questão
    # null=True e blank=True — campo totalmente opcional
    tema = models.ForeignKey(
        Tema,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questoes',
        verbose_name='Tema'
    )

    # Campo de texto longo — armazena o enunciado da questão
    enunciado = models.TextField(
        verbose_name='Enunciado'
    )

    # URL da imagem do enunciado — opcional
    imagem_enunciado = models.URLField(
        blank=True,
        null=True,
        verbose_name='Imagem do Enunciado (URL)',
        help_text='Cole a URL de uma imagem para ilustrar o enunciado (opcional)'
    )

    # Campos das 5 alternativas
    opcao_a = models.CharField(max_length=500, verbose_name='Alternativa A')
    opcao_b = models.CharField(max_length=500, verbose_name='Alternativa B')
    opcao_c = models.CharField(max_length=500, verbose_name='Alternativa C')
    opcao_d = models.CharField(max_length=500, verbose_name='Alternativa D')
    opcao_e = models.CharField(max_length=500, verbose_name='Alternativa E',
                                blank=True, default='')  # ← nova alternativa

    # URLs das imagens das alternativas — todas opcionais
    imagem_opcao_a = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa A (URL)')
    imagem_opcao_b = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa B (URL)')
    imagem_opcao_c = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa C (URL)')
    imagem_opcao_d = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa D (URL)')
    imagem_opcao_e = models.URLField(blank=True, null=True, verbose_name='Imagem Alternativa E (URL)')  # ← nova

    # Campo que armazena qual alternativa é a correta (A, B, C, D ou E)
    resposta_correta = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Resposta Correta'
    )

    # NOVO — Nível de dificuldade
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]
    dificuldade = models.CharField(
        max_length=1,
        choices=DIFICULDADE_CHOICES,
        default='M',
        verbose_name='Dificuldade'
    )

    # NOVO — Explicação do gabarito
    explicacao = models.TextField(
        blank=True,
        verbose_name='Explicação do gabarito'
    )

    # Campo de ordem
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name='Ordem'
    )

    def __str__(self):
        return f'Questão {self.ordem}: {self.enunciado[:50]}...'

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['simulado', 'ordem']