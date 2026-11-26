"""Registro do Funcionário no admin."""
from django.contrib import admin

from funcionarios.models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cargo', 'salario', 'hora_entrada', 'hora_saida')
    list_filter = ('cargo',)
    search_fields = ('nome', 'matricula')
