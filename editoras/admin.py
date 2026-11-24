"""Registro da Editora no admin."""
from django.contrib import admin

from editoras.models import Editora


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cidade', 'email')
    search_fields = ('nome', 'cnpj', 'cidade')
    list_filter = ('cidade',)
