"""Registro do Autor no admin."""
from django.contrib import admin

from autores.models import Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nacionalidade', 'data_nascimento')
    search_fields = ('nome', 'nacionalidade')
    list_filter = ('nacionalidade',)
