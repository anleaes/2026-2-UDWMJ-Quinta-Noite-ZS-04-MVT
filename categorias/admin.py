"""Registro da Categoria no admin."""
from django.contrib import admin

from categorias.models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
