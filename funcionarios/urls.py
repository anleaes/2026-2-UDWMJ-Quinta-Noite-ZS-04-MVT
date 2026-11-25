"""Rotas do app funcionarios."""
from django.urls import path

from funcionarios import views

app_name = 'funcionarios'

urlpatterns = [
    path('', views.funcionario_listar, name='funcionario_listar'),
    path('novo/', views.funcionario_criar, name='funcionario_criar'),
    path('<int:pk>/', views.funcionario_detalhar, name='funcionario_detalhar'),
    path('<int:pk>/editar/', views.funcionario_editar, name='funcionario_editar'),
    path('<int:pk>/excluir/', views.funcionario_excluir, name='funcionario_excluir'),
]
