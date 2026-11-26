"""Rotas do app autores."""
from django.urls import path

from autores import views

app_name = 'autores'

urlpatterns = [
    path('', views.autor_listar, name='autor_listar'),
    path('novo/', views.autor_criar, name='autor_criar'),
    path('<int:pk>/', views.autor_detalhar, name='autor_detalhar'),
    path('<int:pk>/editar/', views.autor_editar, name='autor_editar'),
    path('<int:pk>/excluir/', views.autor_excluir, name='autor_excluir'),
]
