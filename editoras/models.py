"""Model da classe Editora."""
from django.db import models


class Editora(models.Model):
    nome = models.CharField('nome', max_length=150)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    email = models.EmailField('e-mail')
    site = models.URLField('site', blank=True)
    cidade = models.CharField('cidade', max_length=100)

    class Meta:
        ordering = ['nome']
        verbose_name = 'editora'
        verbose_name_plural = 'editoras'

    def __str__(self):
        return self.nome
