from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import ImportacaoProva, ProvaOriginal, QuestaoImportada
from .services import processar_importacao, publicar_questao_importada


@admin.action(description='Aprovar e publicar questões selecionadas')
def aprovar_e_publicar(modeladmin, request, queryset):
    publicadas = 0
    for questao in queryset:
        try:
            publicar_questao_importada(questao)
            publicadas += 1
        except ValidationError as exc:
            modeladmin.message_user(
                request,
                f'Q{questao.numero_na_prova}: {exc}',
                level=messages.WARNING,
            )
    if publicadas:
        modeladmin.message_user(
            request,
            f'{publicadas} questão(ões) publicada(s) com sucesso.',
            level=messages.SUCCESS,
        )


@admin.action(description='Marcar questões selecionadas como correção necessária')
def marcar_correcao_necessaria(modeladmin, request, queryset):
    total = queryset.exclude(status=QuestaoImportada.PUBLICADA).update(
        status=QuestaoImportada.CORRECAO_NECESSARIA,
    )
    modeladmin.message_user(
        request,
        f'{total} questão(ões) marcada(s) para correção.',
        level=messages.SUCCESS,
    )


@admin.action(description='Rejeitar questões selecionadas')
def rejeitar_questoes_importadas(modeladmin, request, queryset):
    total = queryset.exclude(status=QuestaoImportada.PUBLICADA).update(
        status=QuestaoImportada.REJEITADA
    )
    modeladmin.message_user(
        request,
        f'{total} questão(ões) rejeitada(s).',
        level=messages.SUCCESS,
    )


@admin.register(ImportacaoProva)
class ImportacaoProvaAdmin(admin.ModelAdmin):
    list_display = [
        'descricao_importacao',
        'status',
        'total_importadas_admin',
        'total_publicadas_admin',
        'total_correcao_admin',
        'criado_por',
        'criado_em',
    ]
    list_filter = ['status', 'ano', 'dia', 'cor']
    search_fields = ['=ano', 'cor', 'mensagem_erro']
    readonly_fields = ['status', 'mensagem_erro', 'criado_por', 'criado_em', 'atualizado_em']

    fieldsets = (
        ('Metadados', {
            'fields': ('tipo_exame', 'ano', 'dia', 'cor'),
            'description': (
                'Este pipeline e exclusivo para provas oficiais do ENEM. '
                'Use apenas arquivos baixados do portal oficial do INEP: '
                'https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem/provas-e-gabaritos'
            ),
        }),
        ('Arquivos', {
            'fields': ('pdf_prova', 'pdf_gabarito'),
            'description': (
                'Envie obrigatoriamente o PDF da prova e o PDF do gabarito da mesma aplicacao oficial do ENEM.'
            ),
        }),
        ('Processamento', {
            'fields': ('status', 'mensagem_erro', 'criado_por', 'criado_em', 'atualizado_em'),
        }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['tipo_exame'].help_text = 'Importacao restrita a provas oficiais do ENEM.'
        form.base_fields['pdf_prova'].help_text = (
            'Use apenas o PDF da prova oficial baixado no portal do INEP.'
        )
        form.base_fields['pdf_gabarito'].help_text = (
            'Use apenas o PDF do gabarito oficial correspondente, baixado no portal do INEP.'
        )
        return form

    def save_model(self, request, obj, form, change):
        if not obj.criado_por_id:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
        if change:
            return
        try:
            processar_importacao(obj)
            self.message_user(
                request,
                'Importação processada com sucesso. Revise as questões importadas antes de publicar.',
                level=messages.SUCCESS,
            )
        except ValidationError as exc:
            obj.status = ImportacaoProva.FALHOU
            obj.mensagem_erro = str(exc)
            obj.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
            self.message_user(request, str(exc), level=messages.ERROR)
        except Exception as exc:
            obj.status = ImportacaoProva.FALHOU
            obj.mensagem_erro = str(exc)
            obj.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
            self.message_user(
                request,
                f'Falha ao processar a importação: {exc}',
                level=messages.ERROR,
            )

    def delete_model(self, request, obj):
        try:
            super().delete_model(request, obj)
        except ValidationError as exc:
            self.message_user(request, str(exc), level=messages.ERROR)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                obj.delete()
            except ValidationError as exc:
                self.message_user(
                    request,
                    f'{obj}: {exc}',
                    level=messages.ERROR,
                )

    def descricao_importacao(self, obj):
        return f'ENEM {obj.ano} - Dia {obj.dia} - {obj.get_cor_display()}'

    descricao_importacao.short_description = 'Importação'

    def total_importadas_admin(self, obj):
        return obj.total_importadas

    total_importadas_admin.short_description = 'Questões importadas'

    def total_publicadas_admin(self, obj):
        return obj.total_publicadas

    total_publicadas_admin.short_description = 'Publicadas'

    def total_correcao_admin(self, obj):
        return obj.total_correcao_necessaria

    total_correcao_admin.short_description = 'Correção necessária'


@admin.register(ProvaOriginal)
class ProvaOriginalAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'importacao', 'total_questoes_esperado', 'status_editorial']
    list_filter = ['status_editorial', 'importacao__ano', 'importacao__cor']
    search_fields = ['descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(QuestaoImportada)
class QuestaoImportadaAdmin(admin.ModelAdmin):
    list_display = [
        'numero_na_prova',
        'importacao',
        'status',
        'gabarito_oficial',
        'questao_oficial',
        'enunciado_resumido',
    ]
    list_filter = ['status', 'importacao__ano', 'importacao__cor', 'importacao']
    search_fields = ['enunciado', 'texto_bruto', 'motivo_status']
    readonly_fields = ['importacao', 'prova_original', 'texto_bruto', 'questao_oficial', 'criado_em', 'atualizado_em']
    ordering = ['importacao', 'numero_na_prova']
    actions = [aprovar_e_publicar, marcar_correcao_necessaria, rejeitar_questoes_importadas]

    fieldsets = (
        ('Origem', {
            'fields': ('importacao', 'prova_original', 'numero_na_prova', 'status', 'motivo_status', 'questao_oficial'),
        }),
        ('Texto extraído', {
            'fields': ('texto_bruto',),
        }),
        ('Conteúdo revisável', {
            'fields': ('enunciado', 'opcao_a', 'opcao_b', 'opcao_c', 'opcao_d', 'opcao_e', 'gabarito_oficial'),
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
        }),
    )
