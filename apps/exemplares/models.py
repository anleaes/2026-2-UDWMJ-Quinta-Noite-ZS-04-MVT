"""Model da classe Exemplar."""
from django.db import models

from estantes.models import Estante
from livros.models import Livro


class Exemplar(models.Model):
    ESTADOS = [
        ('novo', 'Novo'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('danificado', 'Danificado'),
        ('perdido', 'Perdido'),
    ]

    livro = models.ForeignKey(
        Livro, verbose_name='livro', on_delete=models.PROTECT, related_name='exemplares',
    )
    codigo_tombo = models.CharField('código de tombo', max_length=30, unique=True)
    estado = models.CharField('estado', max_length=15, choices=ESTADOS, default='bom')
    disponivel = models.BooleanField('disponível', default=True)
    data_aquisicao = models.DateField('data de aquisição')
    estante = models.ForeignKey(
        Estante, verbose_name='estante', on_delete=models.PROTECT, related_name='exemplares',
    )

    class Meta:
        ordering = ['codigo_tombo']
        verbose_name = 'exemplar'
        verbose_name_plural = 'exemplares'

    def __str__(self):
        return f'{self.codigo_tombo} — {self.livro.titulo}'

    @property
    def pode_emprestar(self):
        """Só empresta exemplar disponível e que não esteja danificado nem perdido."""
        return self.disponivel and self.estado not in ('danificado', 'perdido')
