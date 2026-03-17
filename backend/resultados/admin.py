# Importa o módulo admin do Django — responsável pelo painel administrativo
from django.contrib import admin

# Importa o model Resultado para registrá-lo no Admin
from .models import Resultado

# O decorator @admin.register substitui o admin.site.register()
@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    """
    Configuração do model Resultado no Django Admin.
    Permite visualizar o desempenho dos alunos nos simulados.
    """

    # Colunas que aparecem na listagem de resultados no Admin
    list_display = ['aluno', 'simulado', 'acertos', 'total_questoes', 'score', 'realizado_em']

    # Filtros disponíveis na barra lateral direita do Admin
    list_filter = ['simulado', 'realizado_em']

    # Campos em que o Admin permite busca por texto
    search_fields = ['aluno__username', 'simulado__titulo']

    # Ordena a listagem pelos mais recentes primeiro
    ordering = ['-realizado_em']

    # Torna os campos somente leitura — resultados não devem ser editados manualmente
    readonly_fields = ['aluno', 'simulado', 'acertos', 'total_questoes', 'score', 'realizado_em']