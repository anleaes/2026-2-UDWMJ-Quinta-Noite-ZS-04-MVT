"""Formulário da Categoria."""
from django import forms

from categorias.models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'slug', 'descricao', 'ativa']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex.: Ficção científica'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Ex.: ficcao-cientifica'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
