# Importa o módulo de URLs do Django
from django.urls import path

# Importa a view de importação
from .views import ImportarQuestoesView

# Define a rota do importador
urlpatterns = [
    # POST /api/importar/ — recebe JSON e cria simulado + questões
    path('', ImportarQuestoesView.as_view(), name='importar'),
]