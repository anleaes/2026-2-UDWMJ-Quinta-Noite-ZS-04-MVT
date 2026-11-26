"""Views CRUD do Empréstimo, com a regra de negócio de empréstimo e devolução."""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from emprestimos.forms import EmprestimoEditarForm, EmprestimoForm
from emprestimos.models import Emprestimo


def emprestimo_listar(request):
    """Lista os empréstimos, destacando os atrasados."""
    emprestimos = Emprestimo.objects.select_related(
        'leitor', 'exemplar__livro', 'funcionario',
    )
    return render(request, 'emprestimos/emprestimo_list.html', {'emprestimos': emprestimos})


def emprestimo_detalhar(request, pk):
    """Exibe os dados de um empréstimo."""
    emprestimo = get_object_or_404(
        Emprestimo.objects.select_related('leitor', 'exemplar__livro', 'funcionario'), pk=pk,
    )
    return render(request, 'emprestimos/emprestimo_detail.html', {'emprestimo': emprestimo})


def emprestimo_criar(request):
    """Registra um novo empréstimo aplicando a regra de negócio."""
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                emprestimo = form.save(commit=False)
                # Prazo automático: 14 dias (professor: 21) e status ativo.
                emprestimo.data_prevista = emprestimo.calcular_data_prevista(timezone.localdate())
                emprestimo.status = Emprestimo.ATIVO
                emprestimo.save()
                # Regra 5: o exemplar deixa de ficar disponível.
                exemplar = emprestimo.exemplar
                exemplar.disponivel = False
                exemplar.save(update_fields=['disponivel'])
            messages.success(
                request,
                f'Empréstimo registrado. Devolução prevista para {emprestimo.data_prevista:%d/%m/%Y}.',
            )
            return redirect('emprestimos:emprestimo_detalhar', pk=emprestimo.pk)
    else:
        form = EmprestimoForm()
    return render(request, 'emprestimos/emprestimo_form.html', {'form': form, 'titulo': 'Novo empréstimo'})


def emprestimo_editar(request, pk):
    """Edita apenas o funcionário responsável (leitor/exemplar exigem devolução)."""
    emprestimo = get_object_or_404(
        Emprestimo.objects.select_related('leitor', 'exemplar__livro'), pk=pk,
    )
    if request.method == 'POST':
        form = EmprestimoEditarForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo atualizado com sucesso.')
            return redirect('emprestimos:emprestimo_detalhar', pk=emprestimo.pk)
    else:
        form = EmprestimoEditarForm(instance=emprestimo)
    return render(
        request,
        'emprestimos/emprestimo_form.html',
        {'form': form, 'titulo': 'Editar empréstimo', 'emprestimo': emprestimo},
    )


def emprestimo_excluir(request, pk):
    """Exclui um empréstimo, após confirmação."""
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        emprestimo.delete()
        messages.success(request, 'Empréstimo excluído com sucesso.')
        return redirect('emprestimos:emprestimo_listar')
    return render(request, 'emprestimos/emprestimo_confirm_delete.html', {'emprestimo': emprestimo})


@require_POST
def emprestimo_devolver(request, pk):
    """Registra a devolução: libera o exemplar, gera multa e atende a reserva."""
    with transaction.atomic():
        emprestimo = get_object_or_404(
            Emprestimo.objects.select_for_update().select_related('exemplar__livro'), pk=pk,
        )
        if emprestimo.data_devolucao is not None:
            messages.warning(request, 'Este empréstimo já foi devolvido.')
            return redirect('emprestimos:emprestimo_detalhar', pk=emprestimo.pk)

        hoje = timezone.localdate()

        # Regra 6: registra a devolução e libera o exemplar.
        emprestimo.data_devolucao = hoje
        emprestimo.status = Emprestimo.DEVOLVIDO
        emprestimo.save(update_fields=['data_devolucao', 'status'])

        exemplar = emprestimo.exemplar
        exemplar.disponivel = True
        exemplar.save(update_fields=['disponivel'])

        # Regra 7: multa de R$ 1,00 por dia de atraso.
        if hoje > emprestimo.data_prevista:
            from multas.models import Multa

            dias_atraso = (hoje - emprestimo.data_prevista).days
            Multa.objects.get_or_create(
                emprestimo=emprestimo,
                defaults={
                    'dias_atraso': dias_atraso,
                    'valor': Multa.calcular_valor(dias_atraso),
                    'paga': False,
                },
            )
            messages.warning(
                request,
                f'Devolução registrada com {dias_atraso} dia(s) de atraso: multa gerada.',
            )

        # Regra 8: a primeira reserva "aguardando" do livro passa a "disponível".
        from reservas.models import Reserva

        reserva = (
            Reserva.objects.filter(livro=exemplar.livro, status=Reserva.AGUARDANDO)
            .order_by('posicao_fila', 'data_reserva', 'pk')
            .first()
        )
        if reserva is not None:
            reserva.status = Reserva.DISPONIVEL
            reserva.save(update_fields=['status'])
            messages.info(
                request,
                f'Reserva de {reserva.leitor.nome} agora está disponível.',
            )

    messages.success(request, 'Devolução registrada com sucesso.')
    return redirect('emprestimos:emprestimo_detalhar', pk=emprestimo.pk)
