from django.urls import path
from gerente.views_limpeza_predial import (gerentes_limpeza_predial, editar_gerente_limpeza_predial,
                                           alterar_status_gerente_limpeza_predial,
                                           historico_de_servicos_gerente_limpeza_predial)


urlpatterns = [
    # rota na raiz do sistema
    path('gerentes_limpeza_predial/<str:userid>', gerentes_limpeza_predial, name='gerentes_limpeza_predial'),
    path(
        'editar_gerente_limpeza_predial/<str:userid>/<str:id_random>',
        editar_gerente_limpeza_predial,
        name='editar_gerente_limpeza_predial'
    ),
    path(
        'alterar_status_gerente_limpeza_predial/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_gerente_limpeza_predial,
        name='alterar_status_gerente_limpeza_predial'
    ),
    path(
        'historico_de_servicos_gerente_limpeza_predial/<str:userid>/<str:id_random>',
        historico_de_servicos_gerente_limpeza_predial,
        name='historico_de_servicos_gerente_limpeza_predial'
    ),
]