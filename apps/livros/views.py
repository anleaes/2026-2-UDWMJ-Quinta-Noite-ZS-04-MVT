"""Views CRUD do Livro (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from livros.forms import LivroForm
from livros.models import Livro


def livro_listar(request):
    """Lista todos os livros cadastrados, em cards com a capa."""
    livros = Livro.objects.prefetch_related('autores').select_related('editora', 'categoria')
    return render(request, 'livros/livro_list.html', {'livros': livros})


def livro_detalhar(request, pk):
    """Exibe os dados de um livro."""
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'livros/livro_detail.html', {'livro': livro})


def livro_criar(request):
    """Cadastra um novo livro (com upload da capa)."""
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso.')
            return redirect('livros:livro_detalhar', pk=livro.pk)
    else:
        form = LivroForm()
    return render(request, 'livros/livro_form.html', {'form': form, 'titulo': 'Novo livro'})


def livro_editar(request, pk):
    """Edita um livro existente."""
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso.')
            return redirect('livros:livro_detalhar', pk=livro.pk)
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/livro_form.html', {'form': form, 'titulo': 'Editar livro'})


def livro_excluir(request, pk):
    """Exclui um livro, após confirmação."""
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso.')
        return redirect('livros:livro_listar')
    return render(request, 'livros/livro_confirm_delete.html', {'livro': livro})
