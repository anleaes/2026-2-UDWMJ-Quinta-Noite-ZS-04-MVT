"""Formulário da Editora."""
from django import forms

from editoras.models import Editora


class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ['nome', 'cnpj', 'email', 'site', 'cidade']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex.: Companhia das Letras'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00', 'data-mascara': 'cnpj'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contato@editora.com.br'}),
            'site': forms.URLInput(attrs={'placeholder': 'https://www.editora.com.br'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Ex.: São Paulo'}),
        }
