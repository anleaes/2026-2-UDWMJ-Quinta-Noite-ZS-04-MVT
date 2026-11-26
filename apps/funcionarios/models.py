"""Model da classe Funcionario."""
from django.db import models


class Funcionario(models.Model):
    BIBLIOTECARIO = 'bibliotecario'
    ATENDENTE = 'atendente'
    AUXILIAR = 'auxiliar'
    GERENTE = 'gerente'

    CARGOS = [
        (BIBLIOTECARIO, 'Bibliotecário'),
        (ATENDENTE, 'Atendente'),
        (AUXILIAR, 'Auxiliar'),
        (GERENTE, 'Gerente'),
    ]

    nome = models.CharField('nome', max_length=150)
    matricula = models.CharField('matrícula', max_length=20, unique=True)
    cargo = models.CharField('cargo', max_length=20, choices=CARGOS)
    salario = models.DecimalField('salário (R$)', max_digits=8, decimal_places=2)
    hora_entrada = models.TimeField('hora de entrada')
    hora_saida = models.TimeField('hora de saída')

    class Meta:
        ordering = ['nome']
        verbose_name = 'funcionário'
        verbose_name_plural = 'funcionários'

    def __str__(self):
        return f'{self.nome} ({self.matricula})'
