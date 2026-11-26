"""Registro da Estante no admin."""
from django.contrib import admin

from estantes.models import Estante


@admin.register(Estante)
class EstanteAdmin(admin.ModelAdmin):
    list_display = ('setor', 'corredor', 'prateleira', 'capacidade', 'largura_metros')
    list_filter = ('setor', 'corredor')
    search_fields = ('setor', 'corredor')
