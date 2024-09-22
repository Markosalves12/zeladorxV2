from django.urls import path
from catalogo_de_servicos.views_jardinagem import (catalogo_de_servicos_jardinagem,
                                                   editar_catalogo_de_servicos_jardinagem,
                                                   alterar_status_catalogo_de_servicos_jardinagem)

urlpatterns = [
    # rota na raiz do sistema
    path(
        'catalogo_de_servicos_jardinagem/<str:userid>',
         catalogo_de_servicos_jardinagem,
        name='catalogo_de_servicos_jardinagem'
    ),
    path(
        'editar_catalogo_de_servicos_jardinagem/<str:userid>/<str:id_random>',
        editar_catalogo_de_servicos_jardinagem,
        name='editar_catalogo_de_servicos_jardinagem'
    ),
    path('alterar_status_catalogo_de_servicos_jardinagem/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_catalogo_de_servicos_jardinagem,
         name='alterar_status_catalogo_de_servicos_jardinagem'
    ),
]
