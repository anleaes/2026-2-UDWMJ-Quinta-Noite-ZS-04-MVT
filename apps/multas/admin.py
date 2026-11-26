"""Registro da Multa no admin."""
from django.contrib import admin

from multas.models import Multa


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ('emprestimo', 'dias_atraso', 'valor', 'paga', 'data_pagamento')
    list_filter = ('paga',)
    search_fields = ('emprestimo__leitor__nome',)
