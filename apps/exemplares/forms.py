"""Formulário do Exemplar."""
from django import forms

from exemplares.models import Exemplar


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = [
            'livro', 'codigo_tombo', 'estado', 'disponivel',
            'data_aquisicao', 'estante',
        ]
        widgets = {
            'codigo_tombo': forms.TextInput(attrs={'placeholder': 'Ex.: T-0001'}),
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),
        }
