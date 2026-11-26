"""Registro da Avaliação no admin."""
from django.contrib import admin

from avaliacoes.models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'leitor', 'nota', 'data')
    list_filter = ('nota',)
    search_fields = ('livro__titulo', 'leitor__nome')
