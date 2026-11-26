"""Rotas globais do projeto `biblioteca`."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('categorias/', include('categorias.urls', namespace='categorias')),
    path('autores/', include('autores.urls', namespace='autores')),
    path('editoras/', include('editoras.urls', namespace='editoras')),
    path('estantes/', include('estantes.urls', namespace='estantes')),
    path('livros/', include('livros.urls', namespace='livros')),
    path('exemplares/', include('exemplares.urls', namespace='exemplares')),
    path('leitores/', include('leitores.urls', namespace='leitores')),
    path('funcionarios/', include('funcionarios.urls', namespace='funcionarios')),
    path('emprestimos/', include('emprestimos.urls', namespace='emprestimos')),
    path('multas/', include('multas.urls', namespace='multas')),
    path('reservas/', include('reservas.urls', namespace='reservas')),
    path('avaliacoes/', include('avaliacoes.urls', namespace='avaliacoes')),
]

# Serve os arquivos de mídia (uploads) apenas em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
