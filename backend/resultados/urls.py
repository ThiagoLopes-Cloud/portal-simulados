# Importa o módulo de URLs do Django
from django.urls import path

# Importa as views de resultado e ranking
from .views import ResultadoListView, ResultadoDetalheView, RankingView

# Define as rotas do app resultados
urlpatterns = [
    # GET /api/resultados — lista todos os resultados do aluno autenticado
    path('', ResultadoListView.as_view(), name='resultado-list'),

    # GET /api/resultados/{id} — retorna o detalhe de um resultado específico
    # <int:pk> — captura o ID da URL como inteiro e passa para a view como 'pk'
    path('<int:pk>/', ResultadoDetalheView.as_view(), name='resultado-detalhe'),

    # GET /api/ranking — retorna o ranking de todos os alunos por score
    path('ranking/', RankingView.as_view(), name='ranking'),
]