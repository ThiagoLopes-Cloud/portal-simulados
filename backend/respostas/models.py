# respostas/models.py
from django.db import models
from users.models import User
from questoes.models import Questao
from simulados.models import Simulado


class Resposta(models.Model):
    """
    Resposta de um aluno a uma questão em uma tentativa específica de um simulado.

    Mudança da Fase 6: unique_together agora inclui 'tentativa'.
    Isso permite que o mesmo aluno responda a mesma questão do mesmo simulado
    em tentativas diferentes — cada tentativa é um conjunto independente de respostas.
    """

    OPCOES_CHOICES = [
        ('A', 'Alternativa A'),
        ('B', 'Alternativa B'),
        ('C', 'Alternativa C'),
        ('D', 'Alternativa D'),
        ('E', 'Alternativa E'),
    ]

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Aluno'
    )

    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Questão'
    )

    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='respostas',
        null=True,
        blank=True,
        verbose_name='Simulado'
    )

    # Número da tentativa — sincronizado com o campo tentativa do Resultado
    # Permite filtrar todas as respostas de uma tentativa específica
    tentativa = models.PositiveIntegerField(
        default=1,
        verbose_name='Tentativa'
    )

    opcao_escolhida = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Opção Escolhida'
    )

    correta = models.BooleanField(
        default=False,
        verbose_name='Correta'
    )

    respondido_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Respondido em'
    )

    def __str__(self):
        return (
            f'{self.aluno.username} → Q{self.questao.id} '
            f'({self.simulado}) T{self.tentativa} → {self.opcao_escolhida}'
        )

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-respondido_em']
        # tentativa incluída — permite múltiplas tentativas do mesmo simulado
        unique_together = ['aluno', 'questao', 'simulado', 'tentativa']