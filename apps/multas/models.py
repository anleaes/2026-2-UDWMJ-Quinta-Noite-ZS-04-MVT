"""Model da classe Multa, gerada automaticamente na devolução com atraso."""
from decimal import Decimal

from django.db import models

from emprestimos.models import Emprestimo


class Multa(models.Model):
    VALOR_POR_DIA = Decimal('1.00')

    emprestimo = models.OneToOneField(
        Emprestimo, verbose_name='empréstimo', on_delete=models.PROTECT, related_name='multas',
    )
    dias_atraso = models.PositiveIntegerField('dias de atraso')
    valor = models.DecimalField('valor (R$)', max_digits=8, decimal_places=2)
    paga = models.BooleanField('paga', default=False)
    data_pagamento = models.DateField('data do pagamento', null=True, blank=True)
    comprovante = models.FileField('comprovante', upload_to='comprovantes/', blank=True, null=True)

    class Meta:
        ordering = ['paga', '-emprestimo__data_devolucao']
        verbose_name = 'multa'
        verbose_name_plural = 'multas'

    def __str__(self):
        return f'Multa de {self.emprestimo.leitor} — R$ {self.valor}'

    @staticmethod
    def calcular_valor(dias_atraso):
        """Valor da multa: R$ 1,00 por dia de atraso."""
        return Multa.VALOR_POR_DIA * dias_atraso
