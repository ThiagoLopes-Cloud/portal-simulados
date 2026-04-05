# Importa o módulo models do Django
from django.db import models

# Importa Tema para vincular a questão a um tópico do ENEM
from conteudo.models import Tema


class Questao(models.Model):
    """
    Representa uma questão do banco de questões.
    IMPORTANTE: não tem FK direto para Simulado.
    O vínculo é feito via SimuladoQuestao (ManyToMany explícito).
    Isso permite reutilizar a mesma questão em múltiplos simulados.
    """

    # Opções de resposta — padrão ENEM com 5 alternativas
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

    # Níveis de dificuldade — usados futuramente na recomendação
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]

    # Relacionamento com tema — nullable pois questões importadas
    # podem não ter tema definido de imediato
    tema = models.ForeignKey(
        Tema,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questoes',
        verbose_name='Tema'
    )

    # Texto principal da questão
    enunciado = models.TextField(
        verbose_name='Enunciado'
    )

    # URL de imagem opcional no enunciado
    imagem_enunciado = models.URLField(
        blank=True,
        null=True,
        verbose_name='Imagem do Enunciado (URL)',
        help_text='Cole a URL de uma imagem para ilustrar o enunciado (opcional)'
    )

    # As 5 alternativas — opcao_e é blank pois questões de 4 alternativas
    # ainda são suportadas (legado)
    opcao_a = models.CharField(max_length=500, verbose_name='Alternativa A')
    opcao_b = models.CharField(max_length=500, verbose_name='Alternativa B')
    opcao_c = models.CharField(max_length=500, verbose_name='Alternativa C')
    opcao_d = models.CharField(max_length=500, verbose_name='Alternativa D')
    opcao_e = models.CharField(
        max_length=500,
        verbose_name='Alternativa E',
        blank=True,
        default=''
    )

    # URLs de imagem para cada alternativa — todas opcionais
    imagem_opcao_a = models.URLField(blank=True, null=True, verbose_name='Imagem A (URL)')
    imagem_opcao_b = models.URLField(blank=True, null=True, verbose_name='Imagem B (URL)')
    imagem_opcao_c = models.URLField(blank=True, null=True, verbose_name='Imagem C (URL)')
    imagem_opcao_d = models.URLField(blank=True, null=True, verbose_name='Imagem D (URL)')
    imagem_opcao_e = models.URLField(blank=True, null=True, verbose_name='Imagem E (URL)')

    # Gabarito — não é exposto na API de prova por segurança
    resposta_correta = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Resposta Correta'
    )

    # Nível de dificuldade — base para futura recomendação
    dificuldade = models.CharField(
        max_length=1,
        choices=DIFICULDADE_CHOICES,
        default='M',
        verbose_name='Dificuldade'
    )

    # Explicação do gabarito — base para gabarito comentado (Fase 5)
    explicacao = models.TextField(
        blank=True,
        verbose_name='Explicação do gabarito'
    )

    # Origem da questão — útil para rastreabilidade
    fonte = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Fonte'
    )

    # Ano de origem — útil para questões do ENEM oficial
    ano_origem = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Ano de Origem'
    )

    idioma = models.CharField(
        max_length=20,
        choices=[
            ('ingles', 'Ingles'),
            ('espanhol', 'Espanhol'),
        ],
        null=True,
        blank=True,
        verbose_name='Idioma'
    )

    importacao_origem = models.ForeignKey(
        'importador.ImportacaoProva',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='questoes_publicadas',
        verbose_name='Importação de Origem'
    )

    prova_original = models.ForeignKey(
        'importador.ProvaOriginal',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='questoes_publicadas',
        verbose_name='Prova Original'
    )

    numero_na_prova = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Número na Prova'
    )

    # CAMPO CRÍTICO — controla se a questão aparece para os alunos
    # False = pendente de revisão (default para questões importadas)
    # True  = aprovada pelo professor, visível na prova
    revisado = models.BooleanField(
        default=False,
        verbose_name='Revisado',
        help_text='Questões não revisadas não aparecem para os alunos'
    )

    # Timestamps automáticos
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    def __str__(self):
        # Exibe os primeiros 60 caracteres do enunciado no Admin
        return f'{self.enunciado[:60]}...'

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        # Ordena por data de criação decrescente — mais recentes primeiro no Admin
        ordering = ['-criado_em']
