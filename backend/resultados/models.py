# resultados/models.py
from django.db import models
from users.models import User
from simulados.models import Simulado


class Resultado(models.Model):
    """
    Representa o resultado de uma tentativa de um aluno em um simulado.

    Mudança da Fase 6: removido unique_together ['aluno', 'simulado'].
    Agora um aluno pode realizar o mesmo simulado múltiplas vezes.
    Cada tentativa gera um Resultado independente com número de tentativa.

    Isso habilita:
    - Histórico de evolução por simulado (Fase 6)
    - Recomendação baseada em padrão de erros ao longo do tempo (Fase 7)
    """

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resultados',
        verbose_name='Aluno'
    )

    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='resultados',
        verbose_name='Simulado'
    )

    # Número sequencial da tentativa — calculado automaticamente na view
    # Tentativa 1 = primeira vez que o aluno fez este simulado
    # Tentativa 2 = segunda vez, e assim por diante
    tentativa = models.PositiveIntegerField(
        default=1,
        verbose_name='Tentativa'
    )

    acertos = models.PositiveIntegerField(
        default=0,
        verbose_name='Acertos'
    )

    total_questoes = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Questões'
    )

    # Score em percentual — ex: 80.00 = 80% de acertos
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Score (%)'
    )

    realizado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Realizado em'
    )

    def __str__(self):
        return (
            f'{self.aluno.username} — {self.simulado.titulo} '
            f'— Tentativa {self.tentativa} — {self.score}%'
        )

    class Meta:
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
        # Mais recentes primeiro
        ordering = ['-realizado_em']
        # unique_together REMOVIDO — permite múltiplas tentativas por simulado
        # Garante que não existe duplicata de tentativa para o mesmo aluno/simulado
        unique_together = ['aluno', 'simulado', 'tentativa']