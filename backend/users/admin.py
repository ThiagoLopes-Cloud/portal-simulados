# Importa o módulo admin do Django — responsável pelo painel administrativo
from django.contrib import admin

# Importa o UserAdmin padrão do Django para reaproveitar suas funcionalidades
from django.contrib.auth.admin import UserAdmin

# Importa nosso model User customizado
from .models import User

# O decorator @admin.register substitui o admin.site.register()
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configuração do model User customizado no Django Admin.
    Herda do UserAdmin padrão e adiciona o campo 'role'.
    """

    # Colunas que aparecem na listagem de usuários no Admin
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']

    # Filtros disponíveis na barra lateral direita do Admin
    list_filter = ['role', 'is_active', 'date_joined']

    # Campos em que o Admin permite busca por texto
    search_fields = ['username', 'email']

    # Ordena a listagem pelos mais recentes primeiro
    ordering = ['-date_joined']

    # Adiciona o campo 'role' na tela de edição do usuário
    # fieldsets herda os campos padrão do UserAdmin e adiciona o nosso campo
    fieldsets = UserAdmin.fieldsets + (
        # Tupla com título da seção e campos extras
        ('Papel no Sistema', {'fields': ('role',)}),
    )

    # Adiciona o campo 'role' na tela de criação de novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Papel no Sistema', {'fields': ('role',)}),
    )