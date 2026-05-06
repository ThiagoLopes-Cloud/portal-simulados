from django.urls import path
from .views import ConcluirAulaView, MateriaisView, TrilhaDetalheView, TrilhasListView

urlpatterns = [
    path("trilhas/", TrilhasListView.as_view(), name="trilhas-list"),
    path("trilhas/<int:pk>/", TrilhaDetalheView.as_view(), name="trilha-detalhe"),
    path("aulas/<int:pk>/concluir/", ConcluirAulaView.as_view(), name="concluir-aula"),
    path("materiais/", MateriaisView.as_view(), name="materiais-list"),
]
