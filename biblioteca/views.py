"""Views gerais do projeto (páginas que não pertencem a um app)."""
from django.shortcuts import render


def inicio(request):
    """Página inicial do sistema de biblioteca."""
    return render(request, 'inicio.html')
