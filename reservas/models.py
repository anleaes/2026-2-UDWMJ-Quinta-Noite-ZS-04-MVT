"""Model da classe Reserva, com cálculo automático da posição na fila."""
from django.db import models

from leitores.models import Leitor
from livros.models import Livro


class Reserva(models.Model):
    AGUARDANDO = 'aguardando'
    DISPONIVEL = 'disponivel'
    CANCELADA = 'cancelada'
    ATENDIDA = 'atendida'

    STATUS = [
        (AGUARDANDO, 'Aguardando'),
        (DISPONIVEL, 'Disponível'),
        (CANCELADA, 'Cancelada'),
        (ATENDIDA, 'Atendida'),
    ]

    leitor = models.ForeignKey(
        Leitor, verbose_name='leitor', on_delete=models.PROTECT, related_name='reservas',
    )
    livro = models.ForeignKey(
        Livro, verbose_name='livro', on_delete=models.PROTECT, related_name='reservas',
    )
    data_reserva = models.DateTimeField('data da reserva', auto_now_add=True)
    posicao_fila = models.PositiveIntegerField('posição na fila', editable=False)
    status = models.CharField('status', max_length=15, choices=STATUS, default=AGUARDANDO)

    class Meta:
        ordering = ['livro', 'posicao_fila']
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'

    def __str__(self):
        return f'{self.leitor} — {self.livro} (#{self.posicao_fila})'

    @staticmethod
    def proxima_posicao(livro):
        """Próxima posição na fila de reserva do livro (última posição + 1)."""
        ultima = Reserva.objects.filter(livro=livro).aggregate(
            maxima=models.Max('posicao_fila'),
        )['maxima']
        return (ultima or 0) + 1

    def save(self, *args, **kwargs):
        """Na criação, calcula a posição na fila automaticamente."""
        if self._state.adding:
            self.posicao_fila = self.proxima_posicao(self.livro)
        super().save(*args, **kwargs)
