"""Model da classe Emprestimo, com a regra de negócio de empréstimo e devolução."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from exemplares.models import Exemplar
from funcionarios.models import Funcionario
from leitores.models import Leitor


class Emprestimo(models.Model):
    # Prazo de devolução, em dias, conforme o tipo de leitor.
    PRAZO_PADRAO_DIAS = 14
    PRAZO_PROFESSOR_DIAS = 21

    ATIVO = 'ativo'
    DEVOLVIDO = 'devolvido'
    ATRASADO = 'atrasado'

    STATUS = [
        (ATIVO, 'Ativo'),
        (DEVOLVIDO, 'Devolvido'),
        (ATRASADO, 'Atrasado'),
    ]

    leitor = models.ForeignKey(
        Leitor, verbose_name='leitor', on_delete=models.PROTECT, related_name='emprestimos',
    )
    exemplar = models.ForeignKey(
        Exemplar, verbose_name='exemplar', on_delete=models.PROTECT, related_name='emprestimos',
    )
    funcionario = models.ForeignKey(
        Funcionario, verbose_name='funcionário', on_delete=models.PROTECT, related_name='emprestimos',
    )
    data_emprestimo = models.DateTimeField('data do empréstimo', auto_now_add=True)
    data_prevista = models.DateField('devolução prevista')
    data_devolucao = models.DateField('data da devolução', null=True, blank=True)
    status = models.CharField('status', max_length=15, choices=STATUS, default=ATIVO)

    class Meta:
        ordering = ['-data_emprestimo']
        verbose_name = 'empréstimo'
        verbose_name_plural = 'empréstimos'

    def __str__(self):
        return f'{self.exemplar} → {self.leitor}'

    @property
    def esta_atrasado(self):
        """Empréstimo ainda aberto com a devolução prevista já vencida."""
        if self.data_devolucao is not None:
            return False
        return self.data_prevista < timezone.localdate()

    def prazo_em_dias(self):
        """Prazo do empréstimo em dias: 21 para professor, 14 para os demais."""
        if self.leitor.tipo == Leitor.PROFESSOR:
            return self.PRAZO_PROFESSOR_DIAS
        return self.PRAZO_PADRAO_DIAS

    def calcular_data_prevista(self, hoje=None):
        """Data prevista de devolução: hoje + prazo do leitor."""
        hoje = hoje or timezone.localdate()
        return hoje + timedelta(days=self.prazo_em_dias())

    def clean(self):
        """Valida as regras 1, 2 e 3 do empréstimo."""
        super().clean()

        if self.data_devolucao is not None:
            # A validação abaixo só se aplica à criação de um novo empréstimo.
            return

        if self.leitor_id and not self.leitor.ativo:
            raise ValidationError({'leitor': 'Este leitor está inativo e não pode emprestar livros.'})

        if self.leitor_id and self.leitor.possui_multa_pendente():
            raise ValidationError({'leitor': 'Este leitor possui multa pendente. Regularize antes de novo empréstimo.'})

        if self.exemplar_id and not self.exemplar.pode_emprestar:
            raise ValidationError({'exemplar': 'Este exemplar não está disponível para empréstimo.'})

        if self.leitor_id and self.data_devolucao is None:
            ativos = Emprestimo.objects.filter(leitor=self.leitor, status__in=(self.ATIVO, self.ATRASADO))
            if self.pk:
                ativos = ativos.exclude(pk=self.pk)
            if ativos.count() >= self.leitor.limite_emprestimos():
                limite = self.leitor.limite_emprestimos()
                raise ValidationError({
                    'leitor': f'Este leitor já atingiu o limite de {limite} empréstimo(s) simultâneo(s).',
                })
