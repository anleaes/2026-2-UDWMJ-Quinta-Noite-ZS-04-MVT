"""Views CRUD da Avaliação."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from avaliacoes.forms import AvaliacaoForm
from avaliacoes.models import Avaliacao


def avaliacao_listar(request):
    """Lista as avaliações dos livros."""
    avaliacoes = Avaliacao.objects.select_related('leitor', 'livro')
    return render(request, 'avaliacoes/avaliacao_list.html', {'avaliacoes': avaliacoes})


def avaliacao_detalhar(request, pk):
    """Exibe os dados de uma avaliação."""
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    return render(request, 'avaliacoes/avaliacao_detail.html', {'avaliacao': avaliacao})


def avaliacao_criar(request):
    """Cria uma avaliação de um livro por um leitor."""
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save()
            messages.success(request, f'Avaliação de "{avaliacao.livro.titulo}" registrada.')
            return redirect('avaliacoes:avaliacao_detalhar', pk=avaliacao.pk)
    else:
        form = AvaliacaoForm()
    return render(request, 'avaliacoes/avaliacao_form.html', {'form': form, 'titulo': 'Nova avaliação'})


def avaliacao_editar(request, pk):
    """Edita uma avaliação existente."""
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avaliação atualizada com sucesso.')
            return redirect('avaliacoes:avaliacao_detalhar', pk=avaliacao.pk)
    else:
        form = AvaliacaoForm(instance=avaliacao)
    return render(request, 'avaliacoes/avaliacao_form.html', {'form': form, 'titulo': 'Editar avaliação'})


def avaliacao_excluir(request, pk):
    """Exclui uma avaliação, após confirmação."""
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    if request.method == 'POST':
        avaliacao.delete()
        messages.success(request, 'Avaliação excluída com sucesso.')
        return redirect('avaliacoes:avaliacao_listar')
    return render(request, 'avaliacoes/avaliacao_confirm_delete.html', {'avaliacao': avaliacao})
