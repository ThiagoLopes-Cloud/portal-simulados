# escolas/admin.py
from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo_convite", "professor", "criado_em")
    search_fields = ("nome", "codigo_convite")
    # Cria uma interface bonitinha para adicionar alunos manualmente se precisar
    filter_horizontal = ("alunos",)
