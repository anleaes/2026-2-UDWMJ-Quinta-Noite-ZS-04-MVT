"""Rotas do app avaliacoes."""
from django.urls import path

from avaliacoes import views

app_name = 'avaliacoes'

urlpatterns = [
    path('', views.avaliacao_listar, name='avaliacao_listar'),
    path('nova/', views.avaliacao_criar, name='avaliacao_criar'),
    path('<int:pk>/', views.avaliacao_detalhar, name='avaliacao_detalhar'),
    path('<int:pk>/editar/', views.avaliacao_editar, name='avaliacao_editar'),
    path('<int:pk>/excluir/', views.avaliacao_excluir, name='avaliacao_excluir'),
]
