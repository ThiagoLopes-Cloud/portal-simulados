# Importa o módulo de URLs do Django
from django.urls import path

# Importa a view de responder simulado
from .views import ResponderView

# Define as rotas do app respostas
urlpatterns = [
    # POST /api/responder — envia as respostas do aluno e calcula o score
    path('', ResponderView.as_view(), name='responder'),
]