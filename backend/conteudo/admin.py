# conteudo/admin.py
from django.contrib import admin
from .models import Materia, Tema, MaterialEstudo


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    # Colunas visíveis na listagem
    list_display = ("id", "nome", "codigo")
    # Permite buscar matérias digitando nome ou código na barra de pesquisa
    search_fields = ("nome", "codigo")


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "materia")
    # O duplo underscore (__) permite pesquisar por campos da tabela estrangeira (Materia)
    search_fields = ("nome", "materia__nome")
    # Cria uma barra lateral direita para filtrar temas por matéria rapidamente
    list_filter = ("materia",)


@admin.register(MaterialEstudo)
class MaterialEstudoAdmin(admin.ModelAdmin):
    # Exibe informações cruciais direto na listagem para gestão rápida
    list_display = ("id", "titulo", "tipo", "tema", "ordem")

    # Permite ao professor buscar pelo título da aula ou pelo nome do tema
    search_fields = ("titulo", "tema__nome")

    # Permite filtrar (barra lateral) para ver apenas "Vídeos" ou apenas materiais de "História"
    list_filter = ("tipo", "tema__materia")

    # Mantém a organização na tela visual idêntica à do banco de dados
    ordering = ("tema", "ordem")
