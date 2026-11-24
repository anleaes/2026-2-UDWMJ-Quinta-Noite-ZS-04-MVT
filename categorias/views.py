"""Views CRUD da Categoria (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from categorias.forms import CategoriaForm
from categorias.models import Categoria


def categoria_listar(request):
    """Lista todas as categorias cadastradas."""
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias})


def categoria_detalhar(request, pk):
    """Exibe os dados de uma categoria."""
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'categorias/categoria_detail.html', {'categoria': categoria})


def categoria_criar(request):
    """Cadastra uma nova categoria."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" cadastrada com sucesso.')
            return redirect('categorias:categoria_detalhar', pk=categoria.pk)
    else:
        form = CategoriaForm()
    return render(request, 'categorias/categoria_form.html', {'form': form, 'titulo': 'Nova categoria'})


def categoria_editar(request, pk):
    """Edita uma categoria existente."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('categorias:categoria_detalhar', pk=categoria.pk)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categoria_form.html', {'form': form, 'titulo': 'Editar categoria'})


def categoria_excluir(request, pk):
    """Exclui uma categoria, após confirmação."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso.')
        return redirect('categorias:categoria_listar')
    return render(request, 'categorias/categoria_confirm_delete.html', {'categoria': categoria})
