from django.urls import path
from servicos.views_configuracoes_limpeza_predial import (configurar_servico_limpeza_predial,
                                                          servicos_configurados_limpeza_predial,
                                                          editar_servico_limpezapredial_configurado)

urlpatterns = [
    path(
        'configurar_servico_limpeza_predial/<str:userid>',
         configurar_servico_limpeza_predial,
         name='configurar_servico_limpeza_predial'
    ),
    path(
        'editar_servico_limpezapredial_configurado/<str:userid>/<str:id_random>',
         editar_servico_limpezapredial_configurado,
         name='editar_servico_limpezapredial_configurado'
    ),
    path(
        'servicos_configurados_limpeza_predial/<str:userid>',
         servicos_configurados_limpeza_predial,
         name='servicos_configurados_limpeza_predial'
    ),
]