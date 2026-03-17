# Importa o módulo models do Django — contém todos os tipos de campos do banco
from django.db import models

# Importa o model Simulado para criar o relacionamento entre questão e simulado
from simulados.models import Simulado

# Define a classe Questao que representa uma tabela no banco de dados
class Questao(models.Model):
    """
    Representa uma questão de múltipla escolha vinculada a um simulado.
    Cada questão tem 4 alternativas (A, B, C, D) e uma resposta correta.
    """

    # Opções de resposta correta disponíveis
    # O primeiro valor é salvo no banco, o segundo é exibido no Admin
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

    # ForeignKey cria relacionamento "muitos para um"
    # Muitas questões podem pertencer a um único simulado
    # on_delete=CASCADE — se o simulado for deletado, suas questões também são
    # related_name — permite acessar as questões de um simulado com simulado.questoes.all()
    simulado = models.ForeignKey(
        Simulado,
        on_delete=models.CASCADE,
        related_name='questoes',
        verbose_name='Simulado'
    )

    # Campo de texto longo — armazena o enunciado da questão
    enunciado = models.TextField(
        verbose_name='Enunciado'
    )

    # Campos de texto curto — armazenam o texto de cada alternativa
    opcao_a = models.CharField(max_length=300, verbose_name='Alternativa A')
    opcao_b = models.CharField(max_length=300, verbose_name='Alternativa B')
    opcao_c = models.CharField(max_length=300, verbose_name='Alternativa C')
    opcao_d = models.CharField(max_length=300, verbose_name='Alternativa D')

    # Campo que armazena qual alternativa é a correta (A, B, C ou D)
    # choices=OPCOES_CHOICES limita os valores aceitos às opções definidas acima
    resposta_correta = models.CharField(
        max_length=1,
        choices=OPCOES_CHOICES,
        verbose_name='Resposta Correta'
    )

    # Campo de ordem para organizar as questões dentro do simulado
    # blank=True e null=True — campo opcional
    ordem = models.PositiveIntegerField(
        default=1,
        verbose_name='Ordem'
    )

    # Método __str__ define como o objeto aparece como texto
    # Mostra os primeiros 50 caracteres do enunciado no Django Admin
    def __str__(self):
        return f'Questão {self.ordem}: {self.enunciado[:50]}...'

    # Classe Meta define configurações extras do model
    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['simulado', 'ordem']  # Ordena por simulado e depois por ordem