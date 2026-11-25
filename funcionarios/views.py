"""Views CRUD do Funcionário (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from funcionarios.forms import FuncionarioForm
from funcionarios.models import Funcionario


def funcionario_listar(request):
    """Lista todos os funcionários cadastrados."""
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionarios/funcionario_list.html', {'funcionarios': funcionarios})


def funcionario_detalhar(request, pk):
    """Exibe os dados de um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, 'funcionarios/funcionario_detail.html', {'funcionario': funcionario})


def funcionario_criar(request):
    """Cadastra um novo funcionário."""
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save()
            messages.success(request, f'Funcionário "{funcionario.nome}" cadastrado com sucesso.')
            return redirect('funcionarios:funcionario_detalhar', pk=funcionario.pk)
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/funcionario_form.html', {'form': form, 'titulo': 'Novo funcionário'})


def funcionario_editar(request, pk):
    """Edita um funcionário existente."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso.')
            return redirect('funcionarios:funcionario_detalhar', pk=funcionario.pk)
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionarios/funcionario_form.html', {'form': form, 'titulo': 'Editar funcionário'})


def funcionario_excluir(request, pk):
    """Exclui um funcionário, após confirmação."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionário excluído com sucesso.')
        return redirect('funcionarios:funcionario_listar')
    return render(request, 'funcionarios/funcionario_confirm_delete.html', {'funcionario': funcionario})
