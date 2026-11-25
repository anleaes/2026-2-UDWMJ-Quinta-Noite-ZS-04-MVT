"""Registro do Leitor no admin."""
from django.contrib import admin

from leitores.models import Leitor


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'tipo', 'email', 'ativo', 'data_cadastro')
    list_filter = ('tipo', 'ativo')
    search_fields = ('nome', 'cpf', 'email')
