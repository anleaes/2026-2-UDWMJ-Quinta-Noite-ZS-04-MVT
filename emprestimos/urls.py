"""Rotas do app emprestimos."""
from django.urls import path

from emprestimos import views

app_name = 'emprestimos'

urlpatterns = [
    path('', views.emprestimo_listar, name='emprestimo_listar'),
    path('novo/', views.emprestimo_criar, name='emprestimo_criar'),
    path('<int:pk>/', views.emprestimo_detalhar, name='emprestimo_detalhar'),
    path('<int:pk>/editar/', views.emprestimo_editar, name='emprestimo_editar'),
    path('<int:pk>/devolver/', views.emprestimo_devolver, name='emprestimo_devolver'),
    path('<int:pk>/excluir/', views.emprestimo_excluir, name='emprestimo_excluir'),
]
