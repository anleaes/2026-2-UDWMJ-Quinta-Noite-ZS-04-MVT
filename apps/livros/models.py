"""Model da classe Livro."""
from django.db import models

from autores.models import Autor
from categorias.models import Categoria
from editoras.models import Editora


class Livro(models.Model):
    titulo = models.CharField('título', max_length=200)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    ano_publicacao = models.IntegerField('ano de publicação')
    num_paginas = models.PositiveIntegerField('número de páginas')
    sinopse = models.TextField('sinopse', blank=True)
    capa = models.ImageField('capa', upload_to='livros/', blank=True, null=True)
    preco_reposicao = models.DecimalField('preço de reposição (R$)', max_digits=8, decimal_places=2)
    autores = models.ManyToManyField(Autor, verbose_name='autores', related_name='livros')
    editora = models.ForeignKey(
        Editora, verbose_name='editora', on_delete=models.PROTECT, related_name='livros',
    )
    categoria = models.ForeignKey(
        Categoria, verbose_name='categoria', on_delete=models.PROTECT, related_name='livros',
    )

    class Meta:
        ordering = ['titulo']
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.titulo
