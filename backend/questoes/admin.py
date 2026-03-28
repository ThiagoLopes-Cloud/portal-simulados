# questoes/admin.py
# Admin do banco de questões — agora as questões são recursos independentes.
# O vínculo com simulados acontece via SimuladoAdmin (inline de SimuladoQuestao).

from django.contrib import admin
from .models import Questao


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    """
    Interface administrativa para o banco de questões.
    Questões são gerenciadas de forma independente de simulados.
    O professor cria questões aqui e as vincula a simulados pelo SimuladoAdmin.
    """

    # Colunas exibidas na listagem
    list_display = [
        'id',
        'tema',
        'dificuldade',
        'enunciado_resumido',
        'resposta_correta',
        'fonte',
        'ano_origem',
        'criado_em',
    ]

    # Filtros laterais para navegação rápida
    list_filter = [
        'dificuldade',
        'resposta_correta',
        'tema__materia',   # Filtra por matéria pai do tema
        'tema',
        'ano_origem',
    ]

    # Campos pesquisáveis por texto
    search_fields = [
        'enunciado',
        'fonte',
        'tema__nome',
        'tema__materia__nome',
    ]

    # Ordena pelo mais recente primeiro
    ordering = ['-criado_em']

    # Organiza os campos do formulário em seções visuais
    fieldsets = (
        ('Conteúdo', {
            'fields': ('tema', 'dificuldade', 'enunciado', 'imagem_enunciado')
        }),
        ('Alternativas', {
            'fields': (
                ('opcao_a', 'imagem_opcao_a'),
                ('opcao_b', 'imagem_opcao_b'),
                ('opcao_c', 'imagem_opcao_c'),
                ('opcao_d', 'imagem_opcao_d'),
                ('opcao_e', 'imagem_opcao_e'),
            )
        }),
        ('Gabarito', {
            'fields': ('resposta_correta', 'explicacao')
        }),
        ('Metadados', {
            'fields': ('fonte', 'ano_origem'),
            'classes': ('collapse',),   # Recolhido por padrão — não polui o form
        }),
    )

    def enunciado_resumido(self, obj):
        """Exibe os primeiros 80 caracteres do enunciado na listagem."""
        return f'{obj.enunciado[:80]}...' if len(obj.enunciado) > 80 else obj.enunciado

    enunciado_resumido.short_description = 'Enunciado'