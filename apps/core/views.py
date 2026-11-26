"""Views do app core: página inicial (painel) do sistema."""
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from emprestimos.models import Emprestimo
from exemplares.models import Exemplar
from livros.models import Livro
from multas.models import Multa
from reservas.models import Reserva


def home(request):
    """Página inicial (painel) com os contadores do acervo e da circulação."""
    template_name = 'core/home.html'
    hoje = timezone.localdate()
    abertos = Q(data_devolucao__isnull=True)
    atrasados = abertos & Q(data_prevista__lt=hoje)

    contadores = {
        'livros': Livro.objects.count(),
        'exemplares_disponiveis': Exemplar.objects.filter(
            disponivel=True,
        ).exclude(estado__in=('danificado', 'perdido')).count(),
        'emprestimos_ativos': Emprestimo.objects.filter(abertos).exclude(atrasados).count(),
        'emprestimos_atrasados': Emprestimo.objects.filter(atrasados).count(),
        'multas_pendentes': Multa.objects.filter(paga=False).count(),
        'reservas_aguardando': Reserva.objects.filter(status=Reserva.AGUARDANDO).count(),
    }

    # Ocupação do acervo: proporção de exemplares disponíveis para empréstimo.
    total_exemplares = Exemplar.objects.count()
    disponiveis = contadores['exemplares_disponiveis']
    ocupacao = {
        'total': total_exemplares,
        'disponiveis': disponiveis,
        'indisponiveis': total_exemplares - disponiveis,
        'percentual_disponivel': round(disponiveis * 100 / total_exemplares) if total_exemplares else 0,
    }

    ultimos_emprestimos = Emprestimo.objects.select_related(
        'leitor', 'exemplar__livro',
    ).order_by('-data_emprestimo')[:5]

    return render(request, template_name, {
        'contadores': contadores,
        'ocupacao': ocupacao,
        'ultimos_emprestimos': ultimos_emprestimos,
    })
