"""Registro da Reserva no admin."""
from django.contrib import admin

from reservas.models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'livro', 'posicao_fila', 'data_reserva', 'status')
    list_filter = ('status',)
    search_fields = ('leitor__nome', 'livro__titulo')
