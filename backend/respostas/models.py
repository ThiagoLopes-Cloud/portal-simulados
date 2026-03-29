# respostas/models.py
from django.db import models
from users.models import User
from questoes.models import Questao
from simulados.models import Simulado


class Resposta(models.Model):
    """
    Resposta de um aluno a uma questão em um simulado específico.
    
    unique_together inclui 'simulado' — permite que a mesma questão
    seja respondida pelo mesmo aluno em simulados diferentes.
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

    # Registra em qual simulado esta resposta foi dada
    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='respostas',
        null=True,
        blank=True,
        verbose_name='Simulado'
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
        return f'{self.aluno.username} → Q{self.questao.id} ({self.simulado}) → {self.opcao_escolhida}'

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-respondido_em']
        unique_together = ['aluno', 'questao', 'simulado']