from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url
import os

# Carrega as variáveis do arquivo .env — só funciona em desenvolvimento local
# Em produção (Railway) as variáveis são injetadas diretamente pelo servidor
load_dotenv()

# BASE_DIR aponta para a pasta raiz do projeto (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Lê a SECRET_KEY do ambiente
# Em desenvolvimento usa o valor do .env
# Em produção usa a variável configurada no Railway
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-apenas-desenvolvimento')

# DEBUG False em produção, True em desenvolvimento
# O Railway injeta DEBUG=False automaticamente
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Permite qualquer domínio acessar o backend
# Em produção futura pode restringir para o domínio do Railway
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',        # Painel administrativo /admin
    'django.contrib.auth',         # Sistema de autenticação
    'django.contrib.contenttypes', # Gerencia tipos de conteúdo
    'django.contrib.sessions',     # Gerencia sessões de usuário
    'django.contrib.messages',     # Sistema de mensagens flash
    'django.contrib.staticfiles',  # Gerencia arquivos estáticos (CSS, JS)

    # Bibliotecas instaladas via pip
    'rest_framework',              # Django REST Framework — cria a API REST
    'rest_framework_simplejwt',    # Autenticação via JWT (tokens)
    'corsheaders',                 # Permite o Vue.js chamar a API (CORS)

    # Apps do nosso projeto
    'users',       # Cadastro, login e perfis de usuário
    'simulados',   # Criação e listagem de simulados
    'questoes',    # Perguntas e alternativas
    'respostas',   # Respostas dos alunos
    'resultados',  # Score e histórico de resultados
    'conteudo',    # Matérias e temas do ENEM
]

MIDDLEWARE = [
    # CorsMiddleware DEVE ser o primeiro — intercepta requisições do Vue.js
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Arquivo principal de rotas do projeto
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Configuração do banco de dados
# Em produção o Railway injeta a variável DATABASE_URL automaticamente
# Em desenvolvimento usa o PostgreSQL local configurado no .env
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/portal_simulados",
        conn_max_age=600,   # Mantém conexões abertas por 600 segundos
        ssl_require=False,  # SSL não obrigatório em desenvolvimento
    )
}

# Diz ao Django para usar nosso modelo User customizado
# em vez do User padrão — permite adicionar o campo 'role'
AUTH_USER_MODEL = 'users.User'

# Configurações globais da API REST
REST_FRAMEWORK = {
    # Define JWT como método padrão de autenticação
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Por padrão todas as rotas exigem autenticação
    # Rotas públicas (login, register) sobrescrevem isso individualmente
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Configurações dos tokens JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),  # Token expira em 8h
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token dura 7 dias
}

# Permite que o Vue.js chame a API sem ser bloqueado pelo browser (CORS)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Desenvolvimento local
]

# Permite qualquer origem temporariamente para o deploy
# Após configurar o domínio do Vercel, substituir por CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True

# Idioma e fuso horário do projeto
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True  # Ativa internacionalização
USE_TZ = True    # Ativa suporte a timezone

# Domínios confiáveis para CSRF — necessário para o Django Admin em produção
CSRF_TRUSTED_ORIGINS = [
    'https://portal-simulados-production.up.railway.app',
    'https://portal-simulados.vercel.app',
]

STATIC_URL = 'static/'

# Define que o campo ID padrão dos models é BigAutoField (inteiro grande)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de arquivos estáticos para produção
# WhiteNoise serve os arquivos estáticos diretamente pelo Django
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'