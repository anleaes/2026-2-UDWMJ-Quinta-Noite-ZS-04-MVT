"""
Configurações para rodar os testes automatizados.

O Oracle Autonomous Database não permite ao Django criar/destruir o banco
de teste, então os testes usam SQLite em memória:

    python manage.py test --settings=biblioteca.settings_test
"""
from biblioteca.settings import *  # noqa: F401,F403

# Banco de teste isolado (SQLite em memória): não toca no Oracle.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

# Senha de usuários de teste mais rápida (não afeta o ambiente real).
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
