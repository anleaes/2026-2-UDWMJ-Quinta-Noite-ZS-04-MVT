"""Formulários do Empréstimo."""
from django import forms

from emprestimos.models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    """Formulário de criação: a data prevista e o status são definidos pela view."""

    class Meta:
        model = Emprestimo
        fields = ['leitor', 'exemplar', 'funcionario']
        help_texts = {
            'exemplar': 'Somente exemplares disponíveis para empréstimo.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            # Na criação, oferece apenas exemplares que a regra permite emprestar.
            self.fields['exemplar'].queryset = self.fields['exemplar'].queryset.filter(
                disponivel=True,
            ).exclude(estado__in=('danificado', 'perdido'))

    def clean(self):
        """Executa as validações da regra de negócio (regras 1, 2 e 3)."""
        dados = super().clean()
        if not self.errors:
            self.instance.clean()
        return dados


class EmprestimoEditarForm(forms.ModelForm):
    """Formulário de edição: só o funcionário responsável pode ser trocado.

    Trocar leitor ou exemplar exige devolver/emprestar, o que mexe na
    disponibilidade do exemplar e na fila de reservas — não é uma edição simples.
    """

    class Meta:
        model = Emprestimo
        fields = ['funcionario']
