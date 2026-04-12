# escolas/urls.py
from django.urls import path
from .views import EntrarNaTurmaView, TurmasProfessorView

urlpatterns = [
    path('entrar/', EntrarNaTurmaView.as_view(), name='entrar-turma'),
    path('minhas-turmas/', TurmasProfessorView.as_view(), name='minhas-turmas'),
]