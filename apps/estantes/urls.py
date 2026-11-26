"""Rotas do app estantes."""
from django.urls import path

from estantes import views

app_name = 'estantes'

urlpatterns = [
    path('', views.estante_listar, name='estante_listar'),
    path('nova/', views.estante_criar, name='estante_criar'),
    path('<int:pk>/', views.estante_detalhar, name='estante_detalhar'),
    path('<int:pk>/editar/', views.estante_editar, name='estante_editar'),
    path('<int:pk>/excluir/', views.estante_excluir, name='estante_excluir'),
]
