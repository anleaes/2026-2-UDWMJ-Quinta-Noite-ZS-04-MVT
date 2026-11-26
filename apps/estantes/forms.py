"""Formulário da Estante."""
from django import forms

from estantes.models import Estante


class EstanteForm(forms.ModelForm):
    class Meta:
        model = Estante
        fields = ['setor', 'corredor', 'prateleira', 'capacidade', 'largura_metros']
        widgets = {
            'setor': forms.TextInput(attrs={'placeholder': 'Ex.: Infantojuvenil'}),
            'corredor': forms.TextInput(attrs={'placeholder': 'Ex.: A'}),
            'prateleira': forms.NumberInput(attrs={'min': 1}),
            'capacidade': forms.NumberInput(attrs={'min': 0}),
            'largura_metros': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
        }
