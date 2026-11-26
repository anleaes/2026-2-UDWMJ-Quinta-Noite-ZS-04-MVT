"""Rotas do app categorias."""
from django.urls import path

from categorias import views

app_name = 'categorias'

urlpatterns = [
    path('', views.categoria_listar, name='categoria_listar'),
    path('nova/', views.categoria_criar, name='categoria_criar'),
    path('<int:pk>/', views.categoria_detalhar, name='categoria_detalhar'),
    path('<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('<int:pk>/excluir/', views.categoria_excluir, name='categoria_excluir'),
]
