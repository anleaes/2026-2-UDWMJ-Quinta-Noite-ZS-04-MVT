"""Rotas do app reservas."""
from django.urls import path

from reservas import views

app_name = 'reservas'

urlpatterns = [
    path('', views.reserva_listar, name='reserva_listar'),
    path('nova/', views.reserva_criar, name='reserva_criar'),
    path('<int:pk>/', views.reserva_detalhar, name='reserva_detalhar'),
    path('<int:pk>/editar/', views.reserva_editar, name='reserva_editar'),
    path('<int:pk>/excluir/', views.reserva_excluir, name='reserva_excluir'),
]
