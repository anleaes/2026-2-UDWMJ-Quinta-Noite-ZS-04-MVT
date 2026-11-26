"""Model da classe Categoria."""
from django.db import models


class Categoria(models.Model):
    nome = models.CharField('nome', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True)
    descricao = models.TextField('descrição', blank=True)
    ativa = models.BooleanField('ativa', default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nome
