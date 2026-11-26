"""Registro do Exemplar no admin."""
from django.contrib import admin

from exemplares.models import Exemplar


@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('codigo_tombo', 'livro', 'estado', 'disponivel', 'estante', 'data_aquisicao')
    list_filter = ('estado', 'disponivel', 'estante')
    search_fields = ('codigo_tombo', 'livro__titulo')
