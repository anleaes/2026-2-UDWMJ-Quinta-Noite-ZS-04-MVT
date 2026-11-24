"""Rotas do app livros."""
from django.urls import path

from livros import views

app_name = 'livros'

urlpatterns = [
    path('', views.livro_listar, name='livro_listar'),
    path('novo/', views.livro_criar, name='livro_criar'),
    path('<int:pk>/', views.livro_detalhar, name='livro_detalhar'),
    path('<int:pk>/editar/', views.livro_editar, name='livro_editar'),
    path('<int:pk>/excluir/', views.livro_excluir, name='livro_excluir'),
]
