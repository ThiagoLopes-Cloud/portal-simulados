# Importa o módulo de URLs do Django
from django.urls import path

# Importa as views de usuário
from .views import RegisterView, ProfileView

# Importa as views de JWT do simplejwt
# TokenObtainPairView — gera o token de acesso e refresh (login)
# TokenRefreshView — gera um novo token de acesso usando o refresh token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define as rotas do app users
# Cada path() define uma URL e qual view ela chama
urlpatterns = [
    # POST /api/register — cadastro de novo usuário
    path('register/', RegisterView.as_view(), name='register'),

    # POST /api/login — login com username e senha, retorna token JWT
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # POST /api/token/refresh — gera novo token usando o refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # GET /api/profile — retorna os dados do usuário autenticado
    path('profile/', ProfileView.as_view(), name='profile'),
]