# simulados/models.py
# Model de Simulado com relacionamento M2M explícito via SimuladoQuestao.
# A tabela intermediária guarda metadados do vínculo (ordem, peso futuro).

from django.db import models
from users.models import User


class Simulado(models.Model):
    """
    Representa uma prova/simulado disponível para os alunos.
    Criado pelo professor e composto por questões do banco via SimuladoQuestao.
    """

    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'
    )

    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    # Quem criou o simulado (professor/admin)
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='simulados_criados',
        verbose_name='Criado por'
    )

    # M2M explícito via tabela intermediária — preserva ordem e metadados
    questoes = models.ManyToManyField(
        'questoes.Questao',
        through='SimuladoQuestao',      # Tabela intermediária com metadados
        through_fields=('simulado', 'questao'),
        related_name='simulados',
        verbose_name='Questões'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    # Controla publicação sem deletar do banco
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    # Data de início e fim opcionais — abre caminho para simulados com prazo
    data_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Início'
    )

    data_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Término'
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Simulado'
        verbose_name_plural = 'Simulados'
        ordering = ['-criado_em']


class SimuladoQuestao(models.Model):
    """
    Tabela intermediária entre Simulado e Questao.
    Guarda metadados do vínculo: ordem da questão no simulado
    e peso futuro (útil para Teoria de Resposta ao Item — TRI).
    
    Esta abordagem é superior ao M2M simples porque:
    - Preserva a ordem das questões por simulado
    - Permite pesos diferentes por questão (pontuação variável)
    - Mantém histórico de qual questão estava em qual posição
    - Facilita relatórios de dificuldade por simulado
    """

    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='simulado_questoes',
        verbose_name='Simulado'
    )

    questao = models.ForeignKey(
        'questoes.Questao',
        on_delete=models.CASCADE,
        related_name='simulado_questoes',
        verbose_name='Questão'
    )

    # Posição da questão dentro deste simulado específico
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name='Ordem'
    )

    # Peso da questão — base para pontuação ponderada futura (TRI)
    # Por ora mantém 1.0 como padrão (todas valem igual)
    peso = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        verbose_name='Peso'
    )

    class Meta:
        verbose_name = 'Questão do Simulado'
        verbose_name_plural = 'Questões do Simulado'

        # Garante que a mesma questão não aparece duas vezes no mesmo simulado
        unique_together = ['simulado', 'questao']

        # Ordenação padrão pela posição da questão
        ordering = ['ordem']

    def __str__(self):
        return f'{self.simulado.titulo} — Q{self.ordem}: {self.questao.enunciado[:40]}...'