# Importa o módulo de URLs do Django
from django.contrib import admin
from django.urls import path, include

# Define as rotas principais do projeto
# include() importa as URLs de cada app
urlpatterns = [
    # Rota do Django Admin — painel administrativo
    path('admin/', admin.site.urls),

    # Rotas de autenticação — login, register, profile, token refresh
    # Todas as rotas do app users ficam sob o prefixo /api/
    path('api/', include('users.urls')),

    # Rotas de simulados — listar e detalhar simulados
    # GET /api/simulados/ e GET /api/simulados/{id}/
    path('api/simulados/', include('simulados.urls')),

    # Rotas de respostas — enviar respostas do aluno
    # POST /api/responder/
    path('api/responder/', include('respostas.urls')),

    # Rotas de resultados e ranking — ver resultados e ranking
    # GET /api/resultados/ e GET /api/ranking/
    path('api/resultados/', include('resultados.urls')),
    
    # Rota de importação de questões via JSON — apenas admins
    path('api/importar/', include('importador.urls')),
]