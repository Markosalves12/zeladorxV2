from django.urls import path
from servicos.views_configuracoes_jardinagem import (configurar_servico_jardinagem,
                                                     servicos_configurados_jardinagem,
                                                     editar_servico_jardinagem_configurado)

urlpatterns = [
    path(
        'configurar_servico_jardinagem/<str:userid>',
         configurar_servico_jardinagem,
         name='configurar_servico_jardinagem'
    ),
    path(
        'editar_servico_jardinagem_configurado/<str:userid>/<str:id_random>',
         editar_servico_jardinagem_configurado,
         name='editar_servico_jardinagem_configurado'
    ),
    path(
        'servicos_configurados_jardinagem/<str:userid>',
         servicos_configurados_jardinagem,
         name='servicos_configurados_jardinagem'
    ),
]