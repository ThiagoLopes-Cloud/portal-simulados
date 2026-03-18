# Importa o módulo de URLs do Django
from django.urls import path

# Importa as views de simulado
from .views import SimuladoListView, SimuladoDetalheView

# Define as rotas do app simulados
urlpatterns = [
    # GET /api/simulados — lista todos os simulados ativos
    path('', SimuladoListView.as_view(), name='simulado-list'),

    # GET /api/simulados/{id} — retorna o detalhe de um simulado com questões
    # <int:pk> — captura o ID da URL como inteiro e passa para a view como 'pk'
    path('<int:pk>/', SimuladoDetalheView.as_view(), name='simulado-detalhe'),
]