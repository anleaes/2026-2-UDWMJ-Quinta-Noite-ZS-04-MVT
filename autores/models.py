"""Model da classe Autor."""
from django.db import models


class Autor(models.Model):
    nome = models.CharField('nome', max_length=150)
    nacionalidade = models.CharField('nacionalidade', max_length=60)
    data_nascimento = models.DateField('data de nascimento')
    biografia = models.TextField('biografia', blank=True)
    foto = models.ImageField('foto', upload_to='autores/', blank=True, null=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return self.nome
