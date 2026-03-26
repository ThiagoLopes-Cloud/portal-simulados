from django.contrib import admin
from .models import Materia, Tema


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome']
    search_fields = ['nome', 'codigo']
    ordering = ['codigo']


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['materia', 'nome']
    list_filter = ['materia']
    search_fields = ['nome']
    ordering = ['materia', 'nome']