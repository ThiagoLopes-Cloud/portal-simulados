# Importa o módulo admin do Django — responsável pelo painel administrativo
from django.contrib import admin

# Importa o model Resposta para registrá-lo no Admin
from .models import Resposta

# O decorator @admin.register substitui o admin.site.register()
@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    """
    Configuração do model Resposta no Django Admin.
    Permite visualizar e filtrar as respostas dos alunos.
    """

    # Colunas que aparecem na listagem de respostas no Admin
    list_display = ['aluno', 'questao', 'opcao_escolhida', 'correta', 'respondido_em']

    # Filtros disponíveis na barra lateral direita do Admin
    list_filter = ['correta', 'respondido_em']

    # Campos em que o Admin permite busca por texto
    search_fields = ['aluno__username', 'questao__enunciado']

    # Ordena a listagem pelas mais recentes primeiro
    ordering = ['-respondido_em']

    # Torna os campos somente leitura — respostas não devem ser editadas manualmente
    readonly_fields = ['aluno', 'questao', 'opcao_escolhida', 'correta', 'respondido_em']