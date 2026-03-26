# Importa o módulo models do Django
from django.db import models


class Materia(models.Model):
    """
    Representa uma disciplina do ENEM.
    ex: Matemática, Língua Portuguesa, Ciências da Natureza
    """

    # Nome completo da matéria
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )

    # Código curto usado internamente ex: MAT, PORT, BIO
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Código'
    )

    def __str__(self):
        return f'{self.codigo} — {self.nome}'

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'
        ordering = ['nome']


class Tema(models.Model):
    """
    Subtópico dentro de uma matéria.
    ex: Funções (MAT), Probabilidade (MAT), Interpretação de Texto (PORT)
    É o nível de granularidade do diagnóstico.
    """

    # Relacionamento com a matéria pai
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='temas',
        verbose_name='Matéria'
    )

    # Nome do tema
    nome = models.CharField(
        max_length=200,
        verbose_name='Nome'
    )

    # Descrição opcional
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    def __str__(self):
        return f'{self.materia.codigo} → {self.nome}'

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        ordering = ['materia', 'nome']