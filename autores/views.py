"""Views CRUD do Autor (baseadas em função)."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from autores.forms import AutorForm
from autores.models import Autor


def autor_listar(request):
    """Lista todos os autores cadastrados."""
    autores = Autor.objects.all()
    return render(request, 'autores/autor_list.html', {'autores': autores})


def autor_detalhar(request, pk):
    """Exibe os dados de um autor."""
    autor = get_object_or_404(Autor, pk=pk)
    return render(request, 'autores/autor_detail.html', {'autor': autor})


def autor_criar(request):
    """Cadastra um novo autor (com upload da foto)."""
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Autor "{autor.nome}" cadastrado com sucesso.')
            return redirect('autores:autor_detalhar', pk=autor.pk)
    else:
        form = AutorForm()
    return render(request, 'autores/autor_form.html', {'form': form, 'titulo': 'Novo autor'})


def autor_editar(request, pk):
    """Edita um autor existente."""
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor atualizado com sucesso.')
            return redirect('autores:autor_detalhar', pk=autor.pk)
    else:
        form = AutorForm(instance=autor)
    return render(request, 'autores/autor_form.html', {'form': form, 'titulo': 'Editar autor'})


def autor_excluir(request, pk):
    """Exclui um autor, após confirmação."""
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        messages.success(request, 'Autor excluído com sucesso.')
        return redirect('autores:autor_listar')
    return render(request, 'autores/autor_confirm_delete.html', {'autor': autor})
