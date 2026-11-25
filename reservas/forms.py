"""Formulário da Reserva."""
from django import forms

from reservas.models import Reserva


class ReservaForm(forms.ModelForm):
    """A posição na fila e o status são calculados pelo sistema."""

    class Meta:
        model = Reserva
        fields = ['leitor', 'livro']
