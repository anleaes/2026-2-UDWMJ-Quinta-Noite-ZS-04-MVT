"""Formulário do Leitor."""
from django import forms

from leitores.models import Leitor


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ['nome', 'cpf', 'email', 'telefone', 'tipo', 'foto', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex.: Maria Silva'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'data-mascara': 'cpf'}),
            'email': forms.EmailInput(attrs={'placeholder': 'maria@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(41) 99999-0000', 'data-mascara': 'telefone'}),
            'foto': forms.ClearableFileInput(attrs={'data-preview': '#preview-foto'}),
        }
