# resultados/urls.py
from django.urls import path
from .views import (
    ResultadoListView,
    ResultadoDetalheView,
    RankingView,
    DashboardView,
    AdminAlunosListView,
    AdminAlunoDashboardView,
)

urlpatterns = [
    path('', ResultadoListView.as_view(), name='resultado-list'),
    path('<int:pk>/', ResultadoDetalheView.as_view(), name='resultado-detalhe'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin/alunos/', AdminAlunosListView.as_view(), name='admin-alunos'),
    path('admin/alunos/<int:pk>/', AdminAlunoDashboardView.as_view(), name='admin-aluno-dashboard'),
]