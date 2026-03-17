# Importa o módulo models do Django — contém todos os tipos de campos do banco
from django.db import models

# Importa o User para saber qual aluno gerou o resultado
from users.models import User

# Importa o Simulado para saber qual prova foi realizada
from simulados.models import Simulado

# Define a classe Resultado que representa uma tabela no banco de dados
class Resultado(models.Model):
    """
    Representa o resultado final de um aluno em um simulado.
    É criado automaticamente após o aluno enviar todas as respostas.
    Armazena o score, total de questões e quantidade de acertos.
    """

    # ForeignKey para o usuário — saber qual aluno realizou o simulado
    # on_delete=CASCADE — se o aluno for deletado, seus resultados também são
    # related_name — permite acessar os resultados de um aluno com user.resultados.all()
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resultados',
        verbose_name='Aluno'
    )

    # ForeignKey para o simulado — saber qual prova foi realizada
    # on_delete=CASCADE — se o simulado for deletado, seus resultados também são
    # related_name — permite acessar os resultados de um simulado com simulado.resultados.all()
    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='resultados',
        verbose_name='Simulado'
    )

    # Quantidade de questões que o aluno acertou
    acertos = models.PositiveIntegerField(
        default=0,
        verbose_name='Acertos'
    )

    # Total de questões do simulado no momento da realização
    total_questoes = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Questões'
    )

    # Score em percentual — ex: 80.00 significa 80% de acertos
    # max_digits=5 — até 5 dígitos no total ex: 100.00
    # decimal_places=2 — 2 casas decimais
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Score (%)'
    )

    # Campo de data e hora — preenchido automaticamente quando o resultado é criado
    realizado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Realizado em'
    )

    # Método __str__ define como o objeto aparece como texto no Django Admin
    def __str__(self):
        return f'{self.aluno.username} — {self.simulado.titulo} — {self.score}%'

    # Classe Meta define configurações extras do model
    class Meta:
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
        ordering = ['-realizado_em']    # Mais recentes primeiro

        # Garante que um aluno só pode ter um resultado por simulado
        unique_together = ['aluno', 'simulado']