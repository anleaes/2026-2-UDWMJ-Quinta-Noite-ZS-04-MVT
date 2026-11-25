"""Registro do Empréstimo no admin."""
from django.contrib import admin

from emprestimos.models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'exemplar', 'funcionario', 'data_emprestimo', 'data_prevista', 'data_devolucao', 'status')
    list_filter = ('status',)
    search_fields = ('leitor__nome', 'exemplar__codigo_tombo')
    date_hierarchy = 'data_emprestimo'
