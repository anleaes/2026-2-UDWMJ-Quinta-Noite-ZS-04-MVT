"""Model da classe Estante."""
from django.db import models


class Estante(models.Model):
    setor = models.CharField('setor', max_length=50)
    corredor = models.CharField('corredor', max_length=50)
    prateleira = models.PositiveIntegerField('prateleira')
    capacidade = models.IntegerField('capacidade (exemplares)')
    largura_metros = models.FloatField('largura (metros)')

    class Meta:
        ordering = ['setor', 'corredor', 'prateleira']
        verbose_name = 'estante'
        verbose_name_plural = 'estantes'

    def __str__(self):
        return f'{self.setor} — corredor {self.corredor} — prateleira {self.prateleira}'
