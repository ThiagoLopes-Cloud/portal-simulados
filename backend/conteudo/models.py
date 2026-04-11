# conteudo/models.py
from django.db import models

# ============================================================
# Modelos Base de Taxonomia (Criados automaticamente no import)
# ============================================================

class Materia(models.Model):
    """
    Representa a disciplina macro. Ex: Matemática, História, Informática.
    """
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Tema(models.Model):
    """
    Representa o subtópico específico dentro de uma matéria. 
    Ex: 'Frações' (Matemática), 'Hardware' (Informática).
    É a base do nosso motor de diagnóstico e recomendação.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='temas')

    def __str__(self):
        return f"{self.materia.codigo} - {self.nome}"


# ============================================================
# Fase 7: Sistema de Recomendação de Conteúdo
# ============================================================

class MaterialEstudo(models.Model):
    """
    Tabela que armazena as aulas, PDFs ou links que serão recomendados
    ao aluno quando ele errar questões de um determinado Tema.
    """
    
    # Definimos os tipos de materiais suportados pela plataforma
    TIPO_CHOICES = [
        ('VIDEO', 'Videoaula (Ex: YouTube)'),
        ('PDF', 'Apostila ou Resumo (PDF)'),
        ('LINK', 'Artigo ou Link Externo'),
    ]
    
    # Relação: Um Tema pode ter VÁRIOS Materiais (1 para N)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='materiais')
    
    titulo = models.CharField(max_length=200, help_text="Ex: Aula 01 - Introdução a Frações")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='VIDEO')
    
    # URLField já valida automaticamente se o link está no formato correto (http://...)
    url = models.URLField(max_length=500, help_text="Link direto para o material")
    
    # Permite ao professor ordenar qual material o aluno deve estudar primeiro
    ordem = models.PositiveIntegerField(default=1, help_text="1 aparece primeiro, 2 depois, etc.")

    class Meta:
        # Garante que as consultas ao banco já retornem ordenadas por padrão
        ordering = ['tema', 'ordem']
        verbose_name = 'Material de Estudo'
        verbose_name_plural = 'Materiais de Estudo'

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo} ({self.tema.nome})"