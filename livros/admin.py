"""Registro do Livro no admin."""
from django.contrib import admin

from livros.models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'editora', 'categoria', 'ano_publicacao', 'preco_reposicao')
    list_filter = ('categoria', 'editora')
    search_fields = ('titulo', 'isbn')
    filter_horizontal = ('autores',)
