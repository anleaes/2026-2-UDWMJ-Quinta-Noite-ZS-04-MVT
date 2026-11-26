"""Formulário do Livro."""
from django import forms

from livros.models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo', 'isbn', 'ano_publicacao', 'num_paginas', 'sinopse',
            'capa', 'preco_reposicao', 'autores', 'editora', 'categoria',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex.: Dom Casmurro'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'Ex.: 9788535910663'}),
            'ano_publicacao': forms.NumberInput(attrs={'min': 1}),
            'num_paginas': forms.NumberInput(attrs={'min': 1}),
            'sinopse': forms.Textarea(attrs={'rows': 4}),
            'preco_reposicao': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'autores': forms.SelectMultiple(attrs={'size': 6}),
            'capa': forms.ClearableFileInput(attrs={'data-preview': '#preview-capa'}),
        }
