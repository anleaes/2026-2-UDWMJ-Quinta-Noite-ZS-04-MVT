"""Rotas do app editoras."""
from django.urls import path

from editoras import views

app_name = 'editoras'

urlpatterns = [
    path('', views.editora_listar, name='editora_listar'),
    path('nova/', views.editora_criar, name='editora_criar'),
    path('<int:pk>/', views.editora_detalhar, name='editora_detalhar'),
    path('<int:pk>/editar/', views.editora_editar, name='editora_editar'),
    path('<int:pk>/excluir/', views.editora_excluir, name='editora_excluir'),
]
