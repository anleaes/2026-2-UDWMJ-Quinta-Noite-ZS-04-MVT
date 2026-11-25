"""Rotas do app exemplares."""
from django.urls import path

from exemplares import views

app_name = 'exemplares'

urlpatterns = [
    path('', views.exemplar_listar, name='exemplar_listar'),
    path('novo/', views.exemplar_criar, name='exemplar_criar'),
    path('<int:pk>/', views.exemplar_detalhar, name='exemplar_detalhar'),
    path('<int:pk>/editar/', views.exemplar_editar, name='exemplar_editar'),
    path('<int:pk>/excluir/', views.exemplar_excluir, name='exemplar_excluir'),
]
