"""Formulário da Multa."""
from django import forms

from multas.models import Multa


class MultaForm(forms.ModelForm):
    """O empréstimo, os dias, o valor e a situação de pagamento são definidos pelo sistema."""

    class Meta:
        model = Multa
        fields = ['comprovante']
        widgets = {
            'comprovante': forms.ClearableFileInput(attrs={'data-preview': '#preview-comprovante'}),
        }
