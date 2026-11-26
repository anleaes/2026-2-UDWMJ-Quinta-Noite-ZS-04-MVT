"""Rotas do app multas."""
from django.urls import path

from multas import views

app_name = 'multas'

urlpatterns = [
    path('', views.multa_listar, name='multa_listar'),
    path('<int:pk>/', views.multa_detalhar, name='multa_detalhar'),
    path('<int:pk>/editar/', views.multa_editar, name='multa_editar'),
    path('<int:pk>/pagar/', views.multa_marcar_paga, name='multa_marcar_paga'),
    path('<int:pk>/excluir/', views.multa_excluir, name='multa_excluir'),
]
