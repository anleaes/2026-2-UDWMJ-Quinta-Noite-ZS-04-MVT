"""Formulário do Autor."""
from django import forms

from autores.models import Autor


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'nacionalidade', 'data_nascimento', 'biografia', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex.: Machado de Assis'}),
            'nacionalidade': forms.TextInput(attrs={'placeholder': 'Ex.: Brasileira'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'biografia': forms.Textarea(attrs={'rows': 4}),
            'foto': forms.ClearableFileInput(attrs={'data-preview': '#preview-foto'}),
        }
