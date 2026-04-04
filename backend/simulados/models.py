# Importa o módulo models do Django
from django.db import models

# Importa o User para saber quem criou o simulado
from users.models import User


class Simulado(models.Model):
    """
    Representa um simulado disponível para os alunos.
    As questões são vinculadas via SimuladoQuestao (ManyToMany explícito),
    o que permite reutilizar questões em múltiplos simulados e
    controlar a ordem de cada questão por simulado.
    """

    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'
    )

    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    # FK para o criador — SET_NULL preserva o simulado se o professor for removido
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='simulados_criados',
        verbose_name='Criado por'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    # Simulado inativo não aparece para os alunos
    # Importador cria simulados como inativo=True por padrão
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    # Datas opcionais — permitem criar simulados com prazo (ex: prova agendada)
    data_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Início'
    )
    data_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Encerramento'
    )

    importacao_origem = models.OneToOneField(
        'importador.ImportacaoProva',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='simulado_original',
        verbose_name='Importação de Origem'
    )

    prova_original = models.ForeignKey(
        'importador.ProvaOriginal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='simulados',
        verbose_name='Prova Original'
    )

    eh_simulado_original = models.BooleanField(
        default=False,
        verbose_name='É Simulado Original'
    )

    # ManyToMany via tabela intermediária SimuladoQuestao
    # through='SimuladoQuestao' diz ao Django para usar nossa tabela customizada
    # em vez de criar uma tabela automática
    questoes = models.ManyToManyField(
        'questoes.Questao',
        through='SimuladoQuestao',
        related_name='simulados',
        verbose_name='Questões'
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Simulado'
        verbose_name_plural = 'Simulados'
        ordering = ['-criado_em']


class SimuladoQuestao(models.Model):
    """
    Tabela intermediária do ManyToMany entre Simulado e Questao.
    Armazena dados específicos do vínculo:
    - ordem: posição da questão neste simulado
    - peso: multiplicador para cálculo TRI futuro (default 1.00)

    Por que tabela explícita em vez de ManyToMany simples?
    Porque precisamos da ordem e do peso — dados que pertencem
    ao VÍNCULO, não à questão nem ao simulado individualmente.
    """

    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='simulado_questoes',
        verbose_name='Simulado'
    )

    # Importa via string para evitar importação circular
    questao = models.ForeignKey(
        'questoes.Questao',
        on_delete=models.CASCADE,
        related_name='simulado_questoes',
        verbose_name='Questão'
    )

    # Posição desta questão dentro deste simulado
    # A mesma questão pode estar na posição 3 em um simulado e na 7 em outro
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name='Ordem'
    )

    # Peso para cálculo TRI futuro — default 1.00 (todas com mesmo peso)
    peso = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        verbose_name='Peso'
    )

    def __str__(self):
        return f'{self.simulado.titulo} — Q{self.ordem}: {self.questao}'

    class Meta:
        verbose_name = 'Questão do Simulado'
        verbose_name_plural = 'Questões do Simulado'
        # Garante que a mesma questão não aparece duas vezes no mesmo simulado
        unique_together = ['simulado', 'questao']
        # Ordena pelo número de ordem dentro de cada simulado
        ordering = ['ordem']
