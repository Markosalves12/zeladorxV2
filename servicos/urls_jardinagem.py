from django.urls import path
from servicos.views_jardinagem import (agendar_servico_jardinagem, editar_servico_jardinagem_agendado,
                                       servicos_agendados_jardinagem,
                                       realizar_servico_jardinagem_agendado, cancelar_servico_jardinagem,
                                       concluir_servico_jardinagem)

urlpatterns = [
    path(
        'agendar_servico_jardinagem/<str:userid>',
        agendar_servico_jardinagem,
        name='agendar_servico_jardinagem'
    ),
    path(
        'editar_servico_jardinagem_agendado/<str:userid>/<str:id_random>',
        editar_servico_jardinagem_agendado,
        name='editar_servico_jardinagem_agendado'
    ),
    path(
        'servicos_agendados_jardinagem/<str:userid>',
        servicos_agendados_jardinagem,
        name='servicos_agendados_jardinagem'
    ),
    path(
        'realizar_servico_jardinagem_agendado/<str:userid>/<str:id_random>',
        realizar_servico_jardinagem_agendado,
        name='realizar_servico_jardinagem_agendado'
    ),
    path(
        'cancelar_servico_jardinagem/<str:userid>/<str:id_random>',
        cancelar_servico_jardinagem,
        name='cancelar_servico_jardinagem'
    ),
    path(
        'concluir_servico_jardinagem/<str:userid>/<str:id_random>',
        concluir_servico_jardinagem,
        name='concluir_servico_jardinagem'
    ),
]