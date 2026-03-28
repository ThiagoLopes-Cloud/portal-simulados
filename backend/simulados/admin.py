# simulados/admin.py
# Admin de Simulado com inline de SimuladoQuestao.
# O professor pode adicionar/remover/reordenar questões diretamente
# na tela de edição do simulado, sem sair da página.

from django.contrib import admin
from .models import Simulado, SimuladoQuestao


class SimuladoQuestaoInline(admin.TabularInline):
    """
    Inline para gerenciar as questões vinculadas ao simulado.
    Exibe o campo 'ordem' e 'peso' para controle fino da prova.
    O campo 'questao' usa raw_id_fields para performance com banco grande.
    """

    model = SimuladoQuestao
    extra = 3                   # Formulários extras para adicionar novas questões
    fields = ['ordem', 'questao', 'peso']
    ordering = ['ordem']

    # raw_id_fields — substitui o select por um campo de busca por ID.
    # Essencial quando o banco tem centenas de questões: evita carregar tudo no select.
    raw_id_fields = ['questao']


@admin.register(Simulado)
class SimuladoAdmin(admin.ModelAdmin):
    """
    Interface administrativa do Simulado.
    Permite gerenciar metadados e questões do simulado em uma única tela.
    """

    list_display = ['titulo', 'criado_por', 'total_questoes', 'criado_em', 'ativo']
    list_filter = ['ativo', 'criado_em']
    list_editable = ['ativo']
    search_fields = ['titulo', 'descricao']
    ordering = ['-criado_em']

    # Inclui o inline de questões diretamente no formulário do simulado
    inlines = [SimuladoQuestaoInline]

    fieldsets = (
        ('Informações do Simulado', {
            'fields': ('titulo', 'descricao', 'criado_por', 'ativo')
        }),
        ('Período de Disponibilidade', {
            'fields': ('data_inicio', 'data_fim'),
            'classes': ('collapse',),
        }),
    )

    def total_questoes(self, obj):
        """Conta as questões vinculadas ao simulado via tabela intermediária."""
        return obj.simulado_questoes.count()

    total_questoes.short_description = 'Questões'


@admin.register(SimuladoQuestao)
class SimuladoQuestaoAdmin(admin.ModelAdmin):
    """
    Admin da tabela intermediária — útil para auditoria e ajustes pontuais.
    Permite visualizar e editar vínculos individualmente.
    """

    list_display = ['simulado', 'ordem', 'questao_resumida', 'peso']
    list_filter = ['simulado']
    ordering = ['simulado', 'ordem']
    raw_id_fields = ['questao']

    def questao_resumida(self, obj):
        return f'{obj.questao.enunciado[:60]}...'

    questao_resumida.short_description = 'Questão'