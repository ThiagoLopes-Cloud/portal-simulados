# Importa o módulo admin do Django
from django.contrib import admin

# Importa o model Questao
from .models import Questao


def aprovar_questoes(modeladmin, request, queryset):
    """
    Ação em lote: marca questões selecionadas como revisado=True.
    Professor seleciona várias questões na listagem e clica nesta ação.
    """
    # update() faz uma única query SQL — muito mais eficiente que salvar um por um
    total = queryset.update(revisado=True)
    # Exibe mensagem de confirmação no topo do Admin
    modeladmin.message_user(request, f'{total} questão(ões) aprovada(s) com sucesso.')

# Texto que aparece no dropdown de ações do Admin
aprovar_questoes.short_description = '✅ Aprovar questões selecionadas'


def rejeitar_questoes(modeladmin, request, queryset):
    """
    Ação em lote: deleta as questões selecionadas permanentemente.
    Use apenas para questões com problemas graves que não valem corrigir.
    Ação irreversível.
    """
    total, _ = queryset.delete()
    modeladmin.message_user(request, f'{total} questão(ões) rejeitada(s) e removida(s).')

rejeitar_questoes.short_description = '❌ Rejeitar e deletar questões selecionadas'


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    """
    Admin do banco de questões.
    Fluxo principal: professor filtra por revisado=False,
    revisa cada questão, seleciona as aprovadas e usa a ação em lote.
    """

    # Colunas visíveis na listagem
    list_display = [
        'enunciado_resumido',
        'tema',
        'dificuldade',
        'resposta_correta',
        'revisado',         # Coluna mais importante — separa pendentes de aprovadas
        'idioma',
        'provas_oficiais_resumidas',
        'fonte',
        'criado_em',
    ]

    # Filtros na barra lateral direita
    list_filter = [
        'revisado',           # Primeiro filtro — o mais usado no fluxo de revisão
        'idioma',
        'dificuldade',
        'tema__materia',      # Filtra por matéria via relacionamento tema → materia
        'fonte',
    ]

    # Busca por texto
    search_fields = ['enunciado', 'tema__nome', 'tema__materia__nome']

    # Permite editar 'revisado' direto na listagem sem abrir a questão
    # Útil para aprovação rápida de questões uma a uma
    list_editable = ['revisado']

    # Ordena pendentes primeiro — revisado=False aparece antes de True
    ordering = ['revisado', '-criado_em']

    # Registra as ações em lote no dropdown
    actions = [aprovar_questoes, rejeitar_questoes]

    readonly_fields = ['provas_oficiais_resumidas']

    # Organiza os campos em seções lógicas no formulário de edição
    fieldsets = (
        ('Conteúdo', {
            'fields': ('enunciado', 'imagem_enunciado', 'tema')
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
            'fields': ('resposta_correta', 'explicacao', 'dificuldade')
        }),
        ('Metadados e Revisão', {
            'fields': ('fonte', 'ano_origem', 'idioma', 'revisado', 'provas_oficiais_resumidas')
        }),
    )

    def enunciado_resumido(self, obj):
        # Exibe apenas os primeiros 80 caracteres para não quebrar o layout da listagem
        return f'{obj.enunciado[:80]}...' if len(obj.enunciado) > 80 else obj.enunciado

    enunciado_resumido.short_description = 'Enunciado'

    def provas_oficiais_resumidas(self, obj):
        ocorrencias = obj.ocorrencias_prova.select_related('prova_original__importacao').order_by(
            'prova_original__importacao__ano',
            'prova_original__importacao__dia',
            'prova_original__importacao__cor',
        )
        if not ocorrencias.exists():
            return 'Sem vinculo com prova oficial'

        itens = []
        for ocorrencia in ocorrencias:
            importacao = ocorrencia.prova_original.importacao
            itens.append(
                f'ENEM {importacao.ano} - Dia {importacao.dia} - {importacao.get_cor_display()}'
                f' ({(ocorrencia.idioma or "geral").title()}) (Q{ocorrencia.numero_na_prova})'
            )
        return ' | '.join(itens)

    provas_oficiais_resumidas.short_description = 'Provas oficiais'
