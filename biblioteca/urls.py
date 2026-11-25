"""Rotas globais do projeto `biblioteca`."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from biblioteca.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('categorias/', include('categorias.urls')),
    path('autores/', include('autores.urls')),
    path('editoras/', include('editoras.urls')),
    path('estantes/', include('estantes.urls')),
    path('livros/', include('livros.urls')),
    path('leitores/', include('leitores.urls')),
    path('funcionarios/', include('funcionarios.urls')),
]

# Serve os arquivos de mídia (uploads) apenas em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
