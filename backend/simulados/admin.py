# Importa o módulo admin do Django — responsável pelo painel administrativo
from django.contrib import admin

# Importa o model Simulado para registrá-lo no Admin
from .models import Simulado

# O decorator @admin.register substitui o admin.site.register()
# É uma forma mais moderna e elegante de registrar models no Admin
@admin.register(Simulado)
class SimuladoAdmin(admin.ModelAdmin):
    """
    Configuração do model Simulado no Django Admin.
    Define quais campos aparecem na listagem e quais filtros estão disponíveis.
    """

    # Colunas que aparecem na listagem de simulados no Admin
    list_display = ['titulo', 'criado_por', 'criado_em', 'ativo']

    # Filtros disponíveis na barra lateral direita do Admin
    list_filter = ['ativo', 'criado_em']

    # Campos em que o Admin permite busca por texto
    search_fields = ['titulo', 'descricao']

    # Permite alterar o campo 'ativo' direto na listagem sem abrir o simulado
    list_editable = ['ativo']

    # Ordena a listagem pelos mais recentes primeiro
    ordering = ['-criado_em']