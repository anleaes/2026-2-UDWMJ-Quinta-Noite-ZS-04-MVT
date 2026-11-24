"""Views CRUD da Editora (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from editoras.forms import EditoraForm
from editoras.models import Editora


def editora_listar(request):
    """Lista todas as editoras cadastradas."""
    editoras = Editora.objects.all()
    return render(request, 'editoras/editora_list.html', {'editoras': editoras})


def editora_detalhar(request, pk):
    """Exibe os dados de uma editora."""
    editora = get_object_or_404(Editora, pk=pk)
    return render(request, 'editoras/editora_detail.html', {'editora': editora})


def editora_criar(request):
    """Cadastra uma nova editora."""
    if request.method == 'POST':
        form = EditoraForm(request.POST)
        if form.is_valid():
            editora = form.save()
            messages.success(request, f'Editora "{editora.nome}" cadastrada com sucesso.')
            return redirect('editoras:editora_detalhar', pk=editora.pk)
    else:
        form = EditoraForm()
    return render(request, 'editoras/editora_form.html', {'form': form, 'titulo': 'Nova editora'})


def editora_editar(request, pk):
    """Edita uma editora existente."""
    editora = get_object_or_404(Editora, pk=pk)
    if request.method == 'POST':
        form = EditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editora atualizada com sucesso.')
            return redirect('editoras:editora_detalhar', pk=editora.pk)
    else:
        form = EditoraForm(instance=editora)
    return render(request, 'editoras/editora_form.html', {'form': form, 'titulo': 'Editar editora'})


def editora_excluir(request, pk):
    """Exclui uma editora, após confirmação."""
    editora = get_object_or_404(Editora, pk=pk)
    if request.method == 'POST':
        editora.delete()
        messages.success(request, 'Editora excluída com sucesso.')
        return redirect('editoras:editora_listar')
    return render(request, 'editoras/editora_confirm_delete.html', {'editora': editora})
