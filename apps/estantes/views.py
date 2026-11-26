"""Views CRUD da Estante (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from estantes.forms import EstanteForm
from estantes.models import Estante


def estante_listar(request):
    """Lista todas as estantes cadastradas."""
    estantes = Estante.objects.all()
    return render(request, 'estantes/estante_list.html', {'estantes': estantes})


def estante_detalhar(request, pk):
    """Exibe os dados de uma estante."""
    estante = get_object_or_404(Estante, pk=pk)
    return render(request, 'estantes/estante_detail.html', {'estante': estante})


def estante_criar(request):
    """Cadastra uma nova estante."""
    if request.method == 'POST':
        form = EstanteForm(request.POST)
        if form.is_valid():
            estante = form.save()
            messages.success(request, f'Estante "{estante}" cadastrada com sucesso.')
            return redirect('estantes:estante_detalhar', pk=estante.pk)
    else:
        form = EstanteForm()
    return render(request, 'estantes/estante_form.html', {'form': form, 'titulo': 'Nova estante'})


def estante_editar(request, pk):
    """Edita uma estante existente."""
    estante = get_object_or_404(Estante, pk=pk)
    if request.method == 'POST':
        form = EstanteForm(request.POST, instance=estante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estante atualizada com sucesso.')
            return redirect('estantes:estante_detalhar', pk=estante.pk)
    else:
        form = EstanteForm(instance=estante)
    return render(request, 'estantes/estante_form.html', {'form': form, 'titulo': 'Editar estante'})


def estante_excluir(request, pk):
    """Exclui uma estante, após confirmação."""
    estante = get_object_or_404(Estante, pk=pk)
    if request.method == 'POST':
        estante.delete()
        messages.success(request, 'Estante excluída com sucesso.')
        return redirect('estantes:estante_listar')
    return render(request, 'estantes/estante_confirm_delete.html', {'estante': estante})
