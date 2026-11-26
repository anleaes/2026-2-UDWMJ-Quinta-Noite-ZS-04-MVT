"""Views CRUD do Leitor (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from leitores.forms import LeitorForm
from leitores.models import Leitor


def leitor_listar(request):
    """Lista todos os leitores cadastrados."""
    leitores = Leitor.objects.all()
    return render(request, 'leitores/leitor_list.html', {'leitores': leitores})


def leitor_detalhar(request, pk):
    """Exibe os dados de um leitor."""
    leitor = get_object_or_404(Leitor, pk=pk)
    return render(request, 'leitores/leitor_detail.html', {'leitor': leitor})


def leitor_criar(request):
    """Cadastra um novo leitor (com upload da foto)."""
    if request.method == 'POST':
        form = LeitorForm(request.POST, request.FILES)
        if form.is_valid():
            leitor = form.save()
            messages.success(request, f'Leitor "{leitor.nome}" cadastrado com sucesso.')
            return redirect('leitores:leitor_detalhar', pk=leitor.pk)
    else:
        form = LeitorForm()
    return render(request, 'leitores/leitor_form.html', {'form': form, 'titulo': 'Novo leitor'})


def leitor_editar(request, pk):
    """Edita um leitor existente."""
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        form = LeitorForm(request.POST, request.FILES, instance=leitor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leitor atualizado com sucesso.')
            return redirect('leitores:leitor_detalhar', pk=leitor.pk)
    else:
        form = LeitorForm(instance=leitor)
    return render(request, 'leitores/leitor_form.html', {'form': form, 'titulo': 'Editar leitor'})


def leitor_excluir(request, pk):
    """Exclui um leitor, após confirmação."""
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.delete()
        messages.success(request, 'Leitor excluído com sucesso.')
        return redirect('leitores:leitor_listar')
    return render(request, 'leitores/leitor_confirm_delete.html', {'leitor': leitor})
