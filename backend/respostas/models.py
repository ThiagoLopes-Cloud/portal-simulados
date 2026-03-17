# Importa o módulo models do Django — contém todos os tipos de campos do banco
from django.db import models

# Importa o User para saber qual aluno respondeu
from users.models import User

# Importa a Questao para saber qual questão foi respondida
from questoes.models import Questao

# Define a classe Resposta que representa uma tabela no banco de dados
class Resposta(models.Model):
    """
    Representa a resposta de um aluno a uma questão específica.
    Cada vez que um aluno responde uma questão, uma Resposta é criada no banco.
    """

    # Opções de resposta disponíveis para o aluno escolher
    OPCAO_A = 'A'
    OPCAO_B = 'B'
    OPCAO_C = 'C'
    OPCAO_D = 'D'

    OPCOES_CHOICES = [
        (OPCAO_A, 'Alternativa A'),
        (OPCAO_B, 'Alternativa B'),
        (OPCAO_C, 'Alternativa C'),
        (OPCAO_D, 'Alternativa D'),
    ]

    # ForeignKey para o usuário — saber qual aluno respondeu
    # on_delete=CASCADE — se o aluno for deletado, suas respostas também são
    # related_name — permite acessar as respostas de um aluno com user.respostas.all()
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Aluno'
    )

    # ForeignKey para a questão — saber qual questão foi respondida
    # on_delete=CASCADE — se a questão for deletada, as respostas também são
    # related_name — permite acessar as respostas de uma questão com questao.respostas.all()
    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Questão'
    )

    # Campo que armazena a alternativa escolhida pelo aluno (A, B, C ou D)
    opcao_escolhida = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Opção Escolhida'
    )

    # Campo calculado — True se a resposta estiver correta, False se errada
    # Será preenchido automaticamente ao comparar com questao.resposta_correta
    correta = models.BooleanField(
        default=False,
        verbose_name='Correta'
    )

    # Campo de data e hora — preenchido automaticamente quando a resposta é criada
    respondido_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Respondido em'
    )

    # Método __str__ define como o objeto aparece como texto no Django Admin
    def __str__(self):
        return f'{self.aluno.username} → Questão {self.questao.id} → {self.opcao_escolhida}'

    # Classe Meta define configurações extras do model
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-respondido_em']   # Mais recentes primeiro

        # Garante que um aluno não pode responder a mesma questão duas vezes
        unique_together = ['aluno', 'questao']
        