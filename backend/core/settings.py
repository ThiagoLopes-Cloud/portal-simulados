from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Lê a SECRET_KEY do .env
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

# Permite qualquer origem em produção
# Em produção final coloque apenas o domínio do Vercel
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',        # desenvolvimento local
]

# Permite qualquer origem temporariamente para o deploy
CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',       # Painel administrativo /admin
    'django.contrib.auth',        # Sistema de autenticação
    'django.contrib.contenttypes',# Gerencia tipos de conteúdo
    'django.contrib.sessions',    # Gerencia sessões de usuário
    'django.contrib.messages',    # Sistema de mensagens flash
    'django.contrib.staticfiles', # Gerencia arquivos estáticos (CSS, JS)

    # Bibliotecas instaladas via pip
    'rest_framework',             # Django REST Framework — cria a API REST
    'rest_framework_simplejwt',   # Autenticação via JWT (tokens)
    'corsheaders',                # Permite o Vue.js chamar a API (CORS)

    # Apps do nosso projeto
    'users',       # Cadastro, login e perfis de usuário
    'simulados',   # Criação e listagem de simulados
    'questoes',    # Perguntas e alternativas
    'respostas',   # Respostas dos alunos
    'resultados',  # Score e histórico de resultados
]

MIDDLEWARE = [
    # CorsMiddleware DEVE ser o primeiro — intercepta requisições do Vue.js
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

# Configuração do banco de dados PostgreSQL
# Substitui 'sua_senha_aqui' pela senha que você definiu na instalação
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Usa PostgreSQL
        'NAME': 'portal_simulados',                # Nome do banco que criamos
        'USER': 'postgres',                        # Usuário padrão do PostgreSQL
        'PASSWORD': os.getenv('DB_PASSWORD'),      # Lê a senha do banco do .env para segurança
        'HOST': 'localhost',                       # Banco rodando na própria máquina
        'PORT': '5432',                            # Porta padrão do PostgreSQL
    }
}

# Diz ao Django para usar nosso modelo User customizado
# em vez do User padrão — permite adicionar o campo 'role'
AUTH_USER_MODEL = 'users.User'

# Configurações globais da API REST
REST_FRAMEWORK = {
    # Define JWT como método padrão de autenticação
    # O aluno envia o token no header de cada requisição
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

# Permite que o Vue.js (rodando na porta 5173) chame a API
# Sem isso o browser bloquearia as requisições por segurança (CORS)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Endereço padrão do Vite (Vue.js)
]

# Idioma e fuso horário do projeto
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True  # Ativa internacionalização
USE_TZ = True    # Ativa suporte a timezone

STATIC_URL = 'static/'

# Define que o campo ID padrão dos models é BigAutoField (inteiro grande)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'