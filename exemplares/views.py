"""Views CRUD do Exemplar (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from exemplares.forms import ExemplarForm
from exemplares.models import Exemplar


def exemplar_listar(request):
    """Lista todos os exemplares cadastrados."""
    exemplares = Exemplar.objects.select_related('livro', 'estante')
    return render(request, 'exemplares/exemplar_list.html', {'exemplares': exemplares})


def exemplar_detalhar(request, pk):
    """Exibe os dados de um exemplar."""
    exemplar = get_object_or_404(Exemplar, pk=pk)
    return render(request, 'exemplares/exemplar_detail.html', {'exemplar': exemplar})


def exemplar_criar(request):
    """Cadastra um novo exemplar."""
    if request.method == 'POST':
        form = ExemplarForm(request.POST)
        if form.is_valid():
            exemplar = form.save()
            messages.success(request, f'Exemplar "{exemplar.codigo_tombo}" cadastrado com sucesso.')
            return redirect('exemplares:exemplar_detalhar', pk=exemplar.pk)
    else:
        form = ExemplarForm()
    return render(request, 'exemplares/exemplar_form.html', {'form': form, 'titulo': 'Novo exemplar'})


def exemplar_editar(request, pk):
    """Edita um exemplar existente."""
    exemplar = get_object_or_404(Exemplar, pk=pk)
    if request.method == 'POST':
        form = ExemplarForm(request.POST, instance=exemplar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exemplar atualizado com sucesso.')
            return redirect('exemplares:exemplar_detalhar', pk=exemplar.pk)
    else:
        form = ExemplarForm(instance=exemplar)
    return render(request, 'exemplares/exemplar_form.html', {'form': form, 'titulo': 'Editar exemplar'})


def exemplar_excluir(request, pk):
    """Exclui um exemplar, após confirmação."""
    exemplar = get_object_or_404(Exemplar, pk=pk)
    if request.method == 'POST':
        exemplar.delete()
        messages.success(request, 'Exemplar excluído com sucesso.')
        return redirect('exemplares:exemplar_listar')
    return render(request, 'exemplares/exemplar_confirm_delete.html', {'exemplar': exemplar})
