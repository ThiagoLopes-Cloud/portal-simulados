# resultados/urls.py
from django.urls import path

from .views import (
    ResultadoListView,
    ResultadoDetalheView,
    RankingView,
    GabaritoView,
    DashboardView,
    AdminAlunosListView,
    AdminAlunoDashboardView,
    EvolucaoSimuladoView,  # ← Adicionado aqui no topo!
)

urlpatterns = [
    # GET /api/resultados/
    path("", ResultadoListView.as_view(), name="resultado-list"),
    # GET /api/resultados/ranking/
    path("ranking/", RankingView.as_view(), name="ranking"),
    # GET /api/resultados/dashboard/
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # GET /api/resultados/admin/alunos/
    path("admin/alunos/", AdminAlunosListView.as_view(), name="admin-alunos"),
    # GET /api/resultados/admin/alunos/{id}/
    path(
        "admin/alunos/<int:pk>/",
        AdminAlunoDashboardView.as_view(),
        name="admin-aluno-dashboard",
    ),
    # GET /api/resultados/evolucao/{simulado_id}/
    # É uma boa prática colocar rotas específicas ANTES das rotas dinâmicas como <int:pk>
    path(
        "evolucao/<int:simulado_id>/",
        EvolucaoSimuladoView.as_view(),
        name="resultado-evolucao",
    ),
    # GET /api/resultados/{id}/
    path("<int:pk>/", ResultadoDetalheView.as_view(), name="resultado-detalhe"),
    # GET /api/resultados/{id}/gabarito/
    path("<int:pk>/gabarito/", GabaritoView.as_view(), name="gabarito"),
]
