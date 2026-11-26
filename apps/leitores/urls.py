"""Rotas do app leitores."""
from django.urls import path

from leitores import views

app_name = 'leitores'

urlpatterns = [
    path('', views.leitor_listar, name='leitor_listar'),
    path('novo/', views.leitor_criar, name='leitor_criar'),
    path('<int:pk>/', views.leitor_detalhar, name='leitor_detalhar'),
    path('<int:pk>/editar/', views.leitor_editar, name='leitor_editar'),
    path('<int:pk>/excluir/', views.leitor_excluir, name='leitor_excluir'),
]
