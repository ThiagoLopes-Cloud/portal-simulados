# Importa o módulo de URLs do Django
from django.urls import path

# Importa todas as views de resultado
from .views import (
    ResultadoListView,
    ResultadoDetalheView,
    RankingView,
    GabaritoView,         # NOVO — Fase 5
    DashboardView,
    AdminAlunosView,
    AdminAlunoDashboardView,
)

# Define as rotas do app resultados
urlpatterns = [

    # GET /api/resultados/
    # Lista todos os resultados do aluno autenticado
    path('', ResultadoListView.as_view(), name='resultado-list'),

    # GET /api/resultados/ranking/
    # Ranking geral de alunos por score
    path('ranking/', RankingView.as_view(), name='ranking'),

    # GET /api/resultados/dashboard/
    # Dashboard de desempenho do aluno autenticado
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # GET /api/resultados/admin/alunos/
    # Lista de alunos com score médio (apenas admin)
    path('admin/alunos/', AdminAlunosView.as_view(), name='admin-alunos'),

    # GET /api/resultados/admin/alunos/{id}/
    # Dashboard individual de um aluno (apenas admin)
    path('admin/alunos/<int:pk>/', AdminAlunoDashboardView.as_view(), name='admin-aluno-dashboard'),

    # GET /api/resultados/{id}/
    # Detalhe de um resultado específico do aluno
    path('<int:pk>/', ResultadoDetalheView.as_view(), name='resultado-detalhe'),

    # GET /api/resultados/{id}/gabarito/
    # NOVO — Fase 5: gabarito comentado com respostas do aluno
    # Retorna questões + resposta correta + explicação + resposta do aluno
    # Também retorna resumo por matéria e temas com erro (base Fase 7)
    path('<int:pk>/gabarito/', GabaritoView.as_view(), name='gabarito'),
]