# Importa o módulo admin do Django — responsável pelo painel administrativo
from django.contrib import admin

# Importa o model Questao para registrá-lo no Admin
from .models import Questao

# TabularInline permite adicionar questões diretamente na tela do Simulado
# Em vez de cadastrar questão por questão separadamente
class QuestaoInline(admin.TabularInline):
    """
    Exibe as questões dentro da tela de edição do Simulado.
    O professor consegue criar várias questões na mesma tela.
    """

    # Model que será exibido inline
    model = Questao

    # Quantidade de formulários vazios extras exibidos para adicionar novas questões
    extra = 3

    # Campos exibidos no formulário inline
    fields = ['ordem', 'enunciado', 'opcao_a', 'opcao_b', 'opcao_c', 'opcao_d', 'resposta_correta']

# O decorator @admin.register substitui o admin.site.register()
@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    """
    Configuração do model Questao no Django Admin.
    """

    # Colunas que aparecem na listagem de questões no Admin
    list_display = ['simulado', 'ordem', 'enunciado_resumido', 'resposta_correta']

    # Filtros disponíveis na barra lateral direita do Admin
    list_filter = ['simulado', 'resposta_correta']

    # Campos em que o Admin permite busca por texto
    search_fields = ['enunciado']

    # Ordena a listagem por simulado e ordem
    ordering = ['simulado', 'ordem']

    # Método que retorna os primeiros 60 caracteres do enunciado
    # Evita que enunciados longos quebrem o layout da listagem
    def enunciado_resumido(self, obj):
        return f'{obj.enunciado[:60]}...'

    # Nome da coluna no Admin
    enunciado_resumido.short_description = 'Enunciado'