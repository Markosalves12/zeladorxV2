from django.urls import path
from catalogo_de_servicos.views_limpeza_predial import (catalogo_de_servicos_limpeza_predial,
                                                        editar_catalogo_de_servicos_limpeza_predial,
                                                        alterar_status_catalogo_de_servicos_limpeza_predial)

urlpatterns = [
    path(
        'catalogo_de_servicos_limpeza_predial/<str:userid>',
        catalogo_de_servicos_limpeza_predial,
        name='catalogo_de_servicos_limpeza_predial'
    ),
    path(
        'editar_catalogo_de_servicos_limpeza_predial/<str:userid>/<str:id_random>',
        editar_catalogo_de_servicos_limpeza_predial,
        name='editar_catalogo_de_servicos_limpeza_predial'
    ),
    path('alterar_status_catalogo_de_servicos_limpeza_predial/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_catalogo_de_servicos_limpeza_predial,
         name='alterar_status_catalogo_de_servicos_limpeza_predial'
    ),
]
