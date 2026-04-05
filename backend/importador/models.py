from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class ImportacaoProva(models.Model):
    ENVIADA = 'enviada'
    PROCESSANDO = 'processando'
    AGUARDANDO_REVISAO = 'aguardando_revisao'
    PARCIALMENTE_PUBLICADA = 'parcialmente_publicada'
    PUBLICADA = 'publicada'
    FALHOU = 'falhou'
    ARQUIVADA = 'arquivada'

    STATUS_CHOICES = [
        (ENVIADA, 'Enviada'),
        (PROCESSANDO, 'Processando'),
        (AGUARDANDO_REVISAO, 'Aguardando revisão'),
        (PARCIALMENTE_PUBLICADA, 'Parcialmente publicada'),
        (PUBLICADA, 'Publicada'),
        (FALHOU, 'Falhou'),
        (ARQUIVADA, 'Arquivada'),
    ]

    ENEM = 'enem'

    TIPO_EXAME_CHOICES = [
        (ENEM, 'ENEM'),
    ]

    DIA_1 = 1
    DIA_2 = 2

    COR_AZUL = 'azul'
    COR_AMARELO = 'amarelo'
    COR_BRANCO = 'branco'
    COR_ROSA = 'rosa'
    COR_CINZA = 'cinza'

    COR_CHOICES = [
        (COR_AZUL, 'Azul'),
        (COR_AMARELO, 'Amarelo'),
        (COR_BRANCO, 'Branco'),
        (COR_ROSA, 'Rosa'),
        (COR_CINZA, 'Cinza'),
    ]

    tipo_exame = models.CharField(
        max_length=20,
        choices=TIPO_EXAME_CHOICES,
        default=ENEM,
        verbose_name='Tipo de exame',
    )
    ano = models.PositiveIntegerField(verbose_name='Ano')
    dia = models.PositiveSmallIntegerField(
        choices=[(DIA_1, 'Dia 1'), (DIA_2, 'Dia 2')],
        verbose_name='Dia',
    )
    cor = models.CharField(
        max_length=20,
        choices=COR_CHOICES,
        verbose_name='Cor do caderno',
    )
    pdf_prova = models.FileField(
        upload_to='importacoes/provas/',
        verbose_name='PDF da prova',
    )
    pdf_gabarito = models.FileField(
        upload_to='importacoes/gabaritos/',
        verbose_name='PDF do gabarito',
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=ENVIADA,
        verbose_name='Status',
    )
    mensagem_erro = models.TextField(
        blank=True,
        verbose_name='Mensagem de erro',
    )
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='importacoes_prova',
        verbose_name='Criado por',
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Importação de Prova'
        verbose_name_plural = 'Importações de Prova'
        ordering = ['-criado_em']

    def __str__(self):
        return f'ENEM {self.ano} - Dia {self.dia} - {self.get_cor_display()}'

    @property
    def total_importadas(self):
        return self.questoes_importadas.count()

    @property
    def total_numeros_importados(self):
        return self.questoes_importadas.values('numero_na_prova').distinct().count()

    @property
    def total_ocorrencias_com_idioma(self):
        return self.questoes_importadas.exclude(idioma__isnull=True).count()

    @property
    def total_pendentes(self):
        return self.questoes_importadas.filter(
            status=QuestaoImportada.PENDENTE_APROVACAO
        ).count()

    @property
    def total_correcao_necessaria(self):
        return self.questoes_importadas.filter(
            status=QuestaoImportada.CORRECAO_NECESSARIA
        ).count()

    @property
    def total_publicadas(self):
        return self.questoes_importadas.filter(
            status=QuestaoImportada.PUBLICADA
        ).count()

    def clean(self):
        if self.tipo_exame != self.ENEM:
            raise ValidationError({'tipo_exame': 'Esta importacao aceita apenas provas oficiais do ENEM.'})
        if not self.pdf_prova:
            raise ValidationError({'pdf_prova': 'Envie o PDF da prova.'})
        if not self.pdf_gabarito:
            raise ValidationError({'pdf_gabarito': 'Envie o PDF do gabarito.'})

    def delete(self, *args, **kwargs):
        try:
            simulado = self.simulado_original
        except Exception:
            simulado = None
        if simulado and simulado.resultados.exists():
            raise ValidationError(
                'Não é possível excluir esta importação porque o simulado original '
                'já possui resultados de alunos.'
            )
        storage = self.pdf_prova.storage if self.pdf_prova else None
        prova_name = self.pdf_prova.name if self.pdf_prova else None
        gabarito_name = self.pdf_gabarito.name if self.pdf_gabarito else None
        super().delete(*args, **kwargs)
        if storage and prova_name:
            storage.delete(prova_name)
        if storage and gabarito_name:
            storage.delete(gabarito_name)


class ProvaOriginal(models.Model):
    RASCUNHO = 'rascunho'
    EM_REVISAO = 'em_revisao'
    PARCIAL = 'parcial'
    COMPLETA = 'completa'

    STATUS_CHOICES = [
        (RASCUNHO, 'Rascunho'),
        (EM_REVISAO, 'Em revisão'),
        (PARCIAL, 'Parcial'),
        (COMPLETA, 'Completa'),
    ]

    importacao = models.OneToOneField(
        ImportacaoProva,
        on_delete=models.CASCADE,
        related_name='prova_original',
        verbose_name='Importação',
    )
    descricao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Descrição',
    )
    total_questoes_esperado = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de questões esperado',
    )
    status_editorial = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=EM_REVISAO,
        verbose_name='Status editorial',
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Prova Original'
        verbose_name_plural = 'Provas Originais'
        ordering = ['-criado_em']

    def __str__(self):
        return self.descricao or str(self.importacao)


class QuestaoImportada(models.Model):
    IDIOMA_INGLES = 'ingles'
    IDIOMA_ESPANHOL = 'espanhol'

    IDIOMA_CHOICES = [
        (IDIOMA_INGLES, 'Ingles'),
        (IDIOMA_ESPANHOL, 'Espanhol'),
    ]

    PENDENTE_APROVACAO = 'pendente_aprovacao'
    CORRECAO_NECESSARIA = 'correcao_necessaria'
    REJEITADA = 'rejeitada'
    PUBLICADA = 'publicada'

    STATUS_CHOICES = [
        (PENDENTE_APROVACAO, 'Pendente de aprovação'),
        (CORRECAO_NECESSARIA, 'Correção necessária'),
        (REJEITADA, 'Rejeitada'),
        (PUBLICADA, 'Publicada'),
    ]

    importacao = models.ForeignKey(
        ImportacaoProva,
        on_delete=models.CASCADE,
        related_name='questoes_importadas',
        verbose_name='Importação',
    )
    prova_original = models.ForeignKey(
        ProvaOriginal,
        on_delete=models.CASCADE,
        related_name='questoes_importadas',
        verbose_name='Prova original',
    )
    numero_na_prova = models.PositiveIntegerField(verbose_name='Número na prova')
    idioma = models.CharField(
        max_length=20,
        choices=IDIOMA_CHOICES,
        null=True,
        blank=True,
        verbose_name='Idioma',
    )
    texto_bruto = models.TextField(blank=True, verbose_name='Texto bruto extraído')
    enunciado = models.TextField(blank=True, verbose_name='Enunciado')
    opcao_a = models.TextField(blank=True, verbose_name='Alternativa A')
    opcao_b = models.TextField(blank=True, verbose_name='Alternativa B')
    opcao_c = models.TextField(blank=True, verbose_name='Alternativa C')
    opcao_d = models.TextField(blank=True, verbose_name='Alternativa D')
    opcao_e = models.TextField(blank=True, verbose_name='Alternativa E')
    gabarito_oficial = models.CharField(
        max_length=1,
        blank=True,
        verbose_name='Gabarito oficial',
    )
    questao_oficial = models.ForeignKey(
        'questoes.Questao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='importacoes_publicadas',
        verbose_name='Questão oficial publicada',
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=PENDENTE_APROVACAO,
        verbose_name='Status',
    )
    motivo_status = models.TextField(blank=True, verbose_name='Motivo do status')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Questão Importada'
        verbose_name_plural = 'Questões Importadas'
        ordering = ['numero_na_prova', 'idioma']
        unique_together = ['importacao', 'numero_na_prova', 'idioma']

    def __str__(self):
        idioma = f' ({self.get_idioma_display()})' if self.idioma else ''
        return f'Q{self.numero_na_prova}{idioma} - {self.importacao}'

    def enunciado_resumido(self):
        if len(self.enunciado) <= 80:
            return self.enunciado
        return f'{self.enunciado[:80]}...'

    enunciado_resumido.short_description = 'Enunciado'


class QuestaoProvaOriginal(models.Model):
    questao = models.ForeignKey(
        'questoes.Questao',
        on_delete=models.CASCADE,
        related_name='ocorrencias_prova',
        verbose_name='Questao',
    )
    prova_original = models.ForeignKey(
        ProvaOriginal,
        on_delete=models.CASCADE,
        related_name='ocorrencias_questao',
        verbose_name='Prova original',
    )
    numero_na_prova = models.PositiveIntegerField(verbose_name='Numero na prova')
    idioma = models.CharField(
        max_length=20,
        choices=QuestaoImportada.IDIOMA_CHOICES,
        null=True,
        blank=True,
        verbose_name='Idioma',
    )
    importacao = models.ForeignKey(
        ImportacaoProva,
        on_delete=models.CASCADE,
        related_name='ocorrencias_questao',
        verbose_name='Importacao',
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Ocorrencia da Questao em Prova'
        verbose_name_plural = 'Ocorrencias da Questao em Provas'
        ordering = ['prova_original__importacao__ano', 'prova_original__importacao__dia', 'numero_na_prova']
        unique_together = [
            ('questao', 'prova_original', 'idioma'),
            ('prova_original', 'numero_na_prova', 'idioma'),
        ]

    def __str__(self):
        idioma = f' / {self.get_idioma_display()}' if self.idioma else ''
        return f'{self.questao_id} em {self.prova_original} (Q{self.numero_na_prova}{idioma})'
