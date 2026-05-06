from django.urls import path
from .views import (
    EntrarNaTurmaView,
    TurmasProfessorView,
    TurmasAlunoView,
    TurmasAlunoOuProfessorView,
    TurmasAdminCreateView,
    TurmaDashboardView,
)

urlpatterns = [
    path("entrar/", EntrarNaTurmaView.as_view(), name="entrar-turma"),
    path("minhas-turmas/", TurmasAlunoOuProfessorView.as_view(), name="minhas-turmas"),
    path("minhas-turmas-aluno/", TurmasAlunoView.as_view(), name="minhas-turmas-aluno"),
    path("turmas/", TurmasAdminCreateView.as_view(), name="criar-turma"),
    path("turmas/<int:turma_id>/dashboard/", TurmaDashboardView.as_view(), name="turma-dashboard"),
]
