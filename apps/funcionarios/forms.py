"""Formulário do Funcionário."""
from django import forms

from funcionarios.models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'matricula', 'cargo', 'salario', 'hora_entrada', 'hora_saida']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex.: João Pereira'}),
            'matricula': forms.TextInput(attrs={'placeholder': 'Ex.: FUNC-0001'}),
            'salario': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
        }
