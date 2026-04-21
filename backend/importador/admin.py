import json

from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR, add_preserved_filters
from django.contrib.admin.utils import quote
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .models import ImportacaoProva, ProvaOriginal, QuestaoImportada, QuestaoProvaOriginal
from .services import processar_importacao, publicar_questao_importada


@admin.action(description='Aprovar e publicar questoes selecionadas')
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
            f'{publicadas} questao(oes) publicada(s) com sucesso.',
            level=messages.SUCCESS,
        )


@admin.action(description='Marcar questoes selecionadas como correcao necessaria')
def marcar_correcao_necessaria(modeladmin, request, queryset):
    total = queryset.exclude(status=QuestaoImportada.PUBLICADA).update(
        status=QuestaoImportada.CORRECAO_NECESSARIA,
    )
    modeladmin.message_user(
        request,
        f'{total} questao(oes) marcada(s) para correcao.',
        level=messages.SUCCESS,
    )


@admin.action(description='Rejeitar questoes selecionadas')
def rejeitar_questoes_importadas(modeladmin, request, queryset):
    total = queryset.exclude(status=QuestaoImportada.PUBLICADA).update(
        status=QuestaoImportada.REJEITADA
    )
    modeladmin.message_user(
        request,
        f'{total} questao(oes) rejeitada(s).',
        level=messages.SUCCESS,
    )


@admin.register(ImportacaoProva)
class ImportacaoProvaAdmin(admin.ModelAdmin):
    list_display = [
        'descricao_importacao',
        'status',
        'total_importadas_admin',
        'total_numeros_admin',
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
            resumo_ocorrencias = (
                f'{obj.total_importadas} ocorrencias importadas '
                f'({obj.total_numeros_importados} numeros de questao'
            )
            if obj.total_ocorrencias_com_idioma:
                resumo_ocorrencias += (
                    f', incluindo {obj.total_ocorrencias_com_idioma} ocorrencias com idioma'
                )
            resumo_ocorrencias += ')'
            if obj.total_correcao_necessaria:
                request._importacao_feedback = {
                    'message': (
                        f'Importacao processada com sucesso: {resumo_ocorrencias}, '
                        f'{obj.total_pendentes} prontas para revisao e '
                        f'{obj.total_correcao_necessaria} com correcao necessaria.'
                    ),
                    'level': messages.WARNING,
                }
            else:
                request._importacao_feedback = {
                    'message': (
                        f'Importacao processada com sucesso: {resumo_ocorrencias} '
                        'e todas prontas para revisao.'
                    ),
                    'level': messages.SUCCESS,
                }
        except ValidationError as exc:
            obj.status = ImportacaoProva.FALHOU
            obj.mensagem_erro = str(exc)
            obj.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
            request._importacao_feedback = {
                'message': f'Falha ao processar a importacao: {exc}',
                'level': messages.ERROR,
            }
        except Exception as exc:
            obj.status = ImportacaoProva.FALHOU
            obj.mensagem_erro = str(exc)
            obj.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
            request._importacao_feedback = {
                'message': f'Falha ao processar a importacao: {exc}',
                'level': messages.ERROR,
            }

    def response_add(self, request, obj, post_url_continue=None):
        feedback = getattr(request, '_importacao_feedback', None)
        if feedback is None:
            return super().response_add(request, obj, post_url_continue=post_url_continue)

        opts = obj._meta
        preserved_filters = self.get_preserved_filters(request)
        preserved_qsl = self._get_preserved_qsl(request, preserved_filters)
        obj_url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_change',
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )

        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            attr = str(to_field) if to_field else obj._meta.pk.attname
            value = obj.serializable_value(attr)
            popup_response_data = json.dumps({'value': str(value), 'obj': str(obj)})
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    f'admin/{opts.app_label}/{opts.model_name}/popup_response.html',
                    f'admin/{opts.app_label}/popup_response.html',
                    'admin/popup_response.html',
                ],
                {'popup_response_data': popup_response_data},
            )

        self.message_user(request, feedback['message'], feedback['level'])

        if '_continue' in request.POST or (
            '_saveasnew' in request.POST
            and self.save_as_continue
            and self.has_change_permission(request, obj)
        ):
            if self.has_change_permission(request, obj):
                self.message_user(
                    request,
                    format_html(
                        'Voce pode revisar esta importacao abaixo: <a href="{}">{}</a>.',
                        obj_url,
                        obj,
                    ),
                    messages.INFO,
                )
            if post_url_continue is None:
                post_url_continue = obj_url
            post_url_continue = add_preserved_filters(
                {
                    'preserved_filters': preserved_filters,
                    'preserved_qsl': preserved_qsl,
                    'opts': opts,
                },
                post_url_continue,
            )
            return HttpResponseRedirect(post_url_continue)

        if '_addanother' in request.POST:
            redirect_url = add_preserved_filters(
                {
                    'preserved_filters': preserved_filters,
                    'preserved_qsl': preserved_qsl,
                    'opts': opts,
                },
                request.path,
            )
            return HttpResponseRedirect(redirect_url)

        return self.response_post_save_add(request, obj)

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
                self.message_user(request, f'{obj}: {exc}', level=messages.ERROR)

    def descricao_importacao(self, obj):
        return f'ENEM {obj.ano} - Dia {obj.dia} - {obj.get_cor_display()}'

    descricao_importacao.short_description = 'Importacao'

    def total_importadas_admin(self, obj):
        return obj.total_importadas

    total_importadas_admin.short_description = 'Ocorrencias importadas'

    def total_numeros_admin(self, obj):
        return obj.total_numeros_importados

    total_numeros_admin.short_description = 'Numeros da prova'

    def total_publicadas_admin(self, obj):
        return obj.total_publicadas

    total_publicadas_admin.short_description = 'Publicadas'

    def total_correcao_admin(self, obj):
        return obj.total_correcao_necessaria

    total_correcao_admin.short_description = 'Correcao necessaria'


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
        'pagina_inicial',
        'idioma',
        'tema',
        'dificuldade',
        'tem_imagem_enunciado',
        'total_imagens_alternativas',
        'importacao',
        'status',
        'gabarito_oficial',
        'questao_oficial',
        'enunciado_resumido',
    ]
    list_filter = [
        'status',
        'idioma',
        'dificuldade',
        'tema__materia',
        'tema',
        'importacao__ano',
        'importacao__cor',
        'importacao',
    ]
    search_fields = ['enunciado', 'texto_bruto', 'motivo_status', 'tema__nome', 'tema__materia__nome']
    readonly_fields = [
        'importacao',
        'prova_original',
        'texto_bruto',
        'questao_oficial',
        'preview_imagem_enunciado',
        'preview_imagens_alternativas',
        'criado_em',
        'atualizado_em',
    ]
    ordering = ['importacao', 'numero_na_prova', 'idioma']
    actions = [aprovar_e_publicar, marcar_correcao_necessaria, rejeitar_questoes_importadas]

    fieldsets = (
        ('Origem', {
            'fields': (
                'importacao',
                'prova_original',
                'numero_na_prova',
                'pagina_inicial',
                'idioma',
                'status',
                'motivo_status',
                'questao_oficial',
            ),
        }),
        ('Texto extraido', {
            'fields': ('texto_bruto',),
        }),
        ('Conteudo revisavel', {
            'fields': (
                'enunciado',
                'tema',
                'opcao_a',
                'opcao_b',
                'opcao_c',
                'opcao_d',
                'opcao_e',
                'gabarito_oficial',
                'dificuldade',
            ),
        }),
        ('Imagem do enunciado', {
            'fields': ('preview_imagem_enunciado', 'imagem_enunciado_arquivo'),
        }),
        ('Imagens das alternativas', {
            'fields': (
                'preview_imagens_alternativas',
                'imagem_opcao_a_arquivo',
                'imagem_opcao_b_arquivo',
                'imagem_opcao_c_arquivo',
                'imagem_opcao_d_arquivo',
                'imagem_opcao_e_arquivo',
            ),
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
        }),
    )

    def tem_imagem_enunciado(self, obj):
        return bool(obj.imagem_enunciado_arquivo)

    tem_imagem_enunciado.boolean = True
    tem_imagem_enunciado.short_description = 'Imagem'

    def total_imagens_alternativas(self, obj):
        return sum(
            bool(image_field)
            for image_field in (
                obj.imagem_opcao_a_arquivo,
                obj.imagem_opcao_b_arquivo,
                obj.imagem_opcao_c_arquivo,
                obj.imagem_opcao_d_arquivo,
                obj.imagem_opcao_e_arquivo,
            )
        )

    total_imagens_alternativas.short_description = 'Imgs alt.'

    def preview_imagem_enunciado(self, obj):
        if not obj.imagem_enunciado_arquivo:
            return 'Sem imagem extraida'
        return format_html(
            '<a href="{0}" target="_blank"><img src="{0}" style="max-width: 360px; max-height: 280px; border: 1px solid #444;" /></a>',
            obj.imagem_enunciado_arquivo.url,
        )

    preview_imagem_enunciado.short_description = 'Preview da imagem'

    def preview_imagens_alternativas(self, obj):
        previews = []
        for letter, image_field in (
            ('A', obj.imagem_opcao_a_arquivo),
            ('B', obj.imagem_opcao_b_arquivo),
            ('C', obj.imagem_opcao_c_arquivo),
            ('D', obj.imagem_opcao_d_arquivo),
            ('E', obj.imagem_opcao_e_arquivo),
        ):
            if not image_field:
                continue
            previews.append(
                format_html(
                    '<div style="display:inline-block; margin: 0 12px 12px 0; text-align:center;">'
                    '<div style="margin-bottom:4px; font-weight:600;">Alternativa {0}</div>'
                    '<a href="{1}" target="_blank"><img src="{1}" style="max-width: 220px; max-height: 180px; border: 1px solid #444;" /></a>'
                    '</div>',
                    letter,
                    image_field.url,
                )
            )
        if not previews:
            return 'Sem imagens extraidas nas alternativas'
        return format_html(''.join(str(preview) for preview in previews))

    preview_imagens_alternativas.short_description = 'Preview das alternativas'


@admin.register(QuestaoProvaOriginal)
class QuestaoProvaOriginalAdmin(admin.ModelAdmin):
    list_display = ['questao', 'prova_original', 'numero_na_prova', 'idioma', 'importacao', 'criado_em']
    list_filter = ['idioma', 'prova_original__importacao__ano', 'prova_original__importacao__cor']
    search_fields = ['questao__enunciado', 'prova_original__descricao']
    readonly_fields = ['criado_em']
