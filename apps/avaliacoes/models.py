"""Model da classe Avaliacao."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from leitores.models import Leitor
from livros.models import Livro


class Avaliacao(models.Model):
    leitor = models.ForeignKey(
        Leitor, verbose_name='leitor', on_delete=models.PROTECT, related_name='avaliacoes',
    )
    livro = models.ForeignKey(
        Livro, verbose_name='livro', on_delete=models.PROTECT, related_name='avaliacoes',
    )
    nota = models.PositiveSmallIntegerField(
        'nota', validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='De 1 a 5.',
    )
    comentario = models.TextField('comentário', blank=True)
    data = models.DateTimeField('data da avaliação', auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'avaliação'
        verbose_name_plural = 'avaliações'

    def __str__(self):
        return f'{self.livro} — {self.nota}★ por {self.leitor}'
