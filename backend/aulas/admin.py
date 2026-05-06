from django.contrib import admin
from .models import Aula, Material, Modulo, ProgressoAluno, Trilha


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    show_change_link = True


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1
    fields = ["titulo", "video_url", "duracao_minutos", "ordem"]


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1
    fields = ["titulo", "tipo", "url_externa", "arquivo"]


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ["nome", "icone", "cor", "ordem"]
    inlines = [ModuloInline]


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ["nome", "trilha", "ordem"]
    list_filter = ["trilha"]
    inlines = [AulaInline, MaterialInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "modulo", "duracao_minutos", "ordem"]
    list_filter = ["modulo__trilha"]
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["titulo", "tipo", "modulo", "aula"]
    list_filter = ["tipo"]


@admin.register(ProgressoAluno)
class ProgressoAlunoAdmin(admin.ModelAdmin):
    list_display = ["aluno", "aula", "is_completed", "concluido_em"]
    list_filter = ["is_completed"]
