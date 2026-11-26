"""Views CRUD da Multa, com a ação de marcar como paga."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from multas.forms import MultaForm
from multas.models import Multa


def multa_listar(request):
    """Lista as multas, mostrando o leitor e a situação de pagamento."""
    multas = Multa.objects.select_related('emprestimo__leitor', 'emprestimo__exemplar__livro')
    return render(request, 'multas/multa_list.html', {'multas': multas})


def multa_detalhar(request, pk):
    """Exibe os dados de uma multa."""
    multa = get_object_or_404(
        Multa.objects.select_related('emprestimo__leitor', 'emprestimo__exemplar__livro'), pk=pk,
    )
    return render(request, 'multas/multa_detail.html', {'multa': multa})


def multa_criar(request):
    """Permite anexar/enviar o comprovante de pagamento de uma multa."""
    if request.method == 'POST':
        form = MultaForm(request.POST, request.FILES)
        if form.is_valid():
            multa = form.save()
            messages.success(request, 'Comprovante da multa registrado com sucesso.')
            return redirect('multas:multa_detalhar', pk=multa.pk)
    else:
        form = MultaForm()
    return render(request, 'multas/multa_form.html', {'form': form, 'titulo': 'Nova multa'})


def multa_editar(request, pk):
    """Edita o comprovante de uma multa existente."""
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == 'POST':
        form = MultaForm(request.POST, request.FILES, instance=multa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Multa atualizada com sucesso.')
            return redirect('multas:multa_detalhar', pk=multa.pk)
    else:
        form = MultaForm(instance=multa)
    return render(request, 'multas/multa_form.html', {'form': form, 'titulo': 'Editar multa'})


def multa_excluir(request, pk):
    """Exclui uma multa, após confirmação."""
    multa = get_object_or_404(Multa, pk=pk)
    if request.method == 'POST':
        multa.delete()
        messages.success(request, 'Multa excluída com sucesso.')
        return redirect('multas:multa_listar')
    return render(request, 'multas/multa_confirm_delete.html', {'multa': multa})


@require_POST
def multa_marcar_paga(request, pk):
    """Marca a multa como paga, registrando a data do pagamento."""
    multa = get_object_or_404(Multa, pk=pk)
    if multa.paga:
        messages.warning(request, 'Esta multa já está marcada como paga.')
    else:
        multa.paga = True
        multa.data_pagamento = timezone.localdate()
        multa.save(update_fields=['paga', 'data_pagamento'])
        messages.success(request, 'Multa marcada como paga.')
    return redirect('multas:multa_detalhar', pk=multa.pk)
