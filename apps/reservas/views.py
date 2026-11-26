"""Views CRUD da Reserva."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from reservas.forms import ReservaForm
from reservas.models import Reserva


def reserva_listar(request):
    """Lista todas as reservas, agrupadas por livro e posição na fila."""
    reservas = Reserva.objects.select_related('leitor', 'livro')
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})


def reserva_detalhar(request, pk):
    """Exibe os dados de uma reserva."""
    reserva = get_object_or_404(Reserva, pk=pk)
    return render(request, 'reservas/reserva_detail.html', {'reserva': reserva})


def reserva_criar(request):
    """Cria uma reserva, posicionando o leitor no fim da fila do livro."""
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            messages.success(
                request,
                f'Reserva registrada: posição {reserva.posicao_fila} na fila de "{reserva.livro.titulo}".',
            )
            return redirect('reservas:reserva_detalhar', pk=reserva.pk)
    else:
        form = ReservaForm()
    return render(request, 'reservas/reserva_form.html', {'form': form, 'titulo': 'Nova reserva'})


def reserva_editar(request, pk):
    """Edita o leitor ou o livro de uma reserva."""
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva atualizada com sucesso.')
            return redirect('reservas:reserva_detalhar', pk=reserva.pk)
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/reserva_form.html', {'form': form, 'titulo': 'Editar reserva'})


def reserva_excluir(request, pk):
    """Exclui uma reserva, após confirmação."""
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso.')
        return redirect('reservas:reserva_listar')
    return render(request, 'reservas/reserva_confirm_delete.html', {'reserva': reserva})
