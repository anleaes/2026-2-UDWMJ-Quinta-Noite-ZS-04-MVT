"""
Configurações do projeto Django `biblioteca`.

Lê os dados sensíveis (SECRET_KEY e credenciais do Oracle) do arquivo `.env`,
que fica fora do Git. Veja `.env.example` para o modelo.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Caminho base do projeto (onde fica o manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega as variáveis do .env (não sobrescreve as já definidas no ambiente).
load_dotenv(BASE_DIR / '.env')


def env(nome, padrao=None):
    """Lê uma variável de ambiente, com valor padrão opcional."""
    return os.environ.get(nome, padrao)


# Segurança
SECRET_KEY = env('SECRET_KEY', 'django-insecure-sem-chave-no-env')

DEBUG = env('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Aplicações
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps do projeto (uma linha por app)
    'categorias',
    'autores',
    'editoras',
    'estantes',
    'livros',
    'exemplares',
    'leitores',
    'funcionarios',
    'emprestimos',
    'reservas',
    'avaliacoes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'biblioteca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'biblioteca.wsgi.application'


# Banco de dados — Oracle Autonomous Database (OCI), mTLS, modo thin.
# Todas as credenciais vêm do .env; a wallet fica fora do repositório.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': env('ORACLE_DSN', ''),
        'USER': env('ORACLE_USER', ''),
        'PASSWORD': env('ORACLE_PASSWORD', ''),
        'OPTIONS': {
            # config_dir: pasta onde está o tnsnames.ora (permite usar o alias
            # "modeloappdb_low" como DSN).
            'config_dir': env('ORACLE_WALLET_DIR', ''),
            # wallet_location: pasta da wallet (mTLS obrigatório).
            'wallet_location': env('ORACLE_WALLET_DIR', ''),
            'wallet_password': env('ORACLE_WALLET_PASSWORD', ''),
        },
    }
}


# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalização
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Arquivos estáticos (CSS, JavaScript, imagens do projeto)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Arquivos enviados pelos usuários (capas, fotos, comprovantes) — fora do Git
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Tipo padrão das chaves primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
