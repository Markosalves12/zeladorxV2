from django.urls import path
from servicos.views_jardinagem import (agendar_servico_jardinagem, editar_servico_jardinagem_agendado,
                                       servicos_agendados_jardinagem,
                                       realizar_servico_jardinagem_agendado, cancelar_servico_jardinagem,
                                       concluir_servico_jardinagem)

urlpatterns = [
    path(
        'agendar-servico-jardinagem/<str:userid>',
        agendar_servico_jardinagem,
        name='agendar_servico_jardinagem'
    ),
    path(
        'editar-servico-jardinagem-agendado/<str:userid>/<str:id_random>',
        editar_servico_jardinagem_agendado,
        name='editar_servico_jardinagem_agendado'
    ),
    path(
        'servicos-agendados-jardinagem/<str:userid>',
        servicos_agendados_jardinagem,
        name='servicos_agendados_jardinagem'
    ),
    path(
        'realizar-servico-jardinagem-agendado/<str:userid>/<str:id_random>',
        realizar_servico_jardinagem_agendado,
        name='realizar_servico_jardinagem_agendado'
    ),
    path(
        'cancelar-servico-jardinagem/<str:userid>/<str:id_random>/<str:type>',
        cancelar_servico_jardinagem,
        name='cancelar_servico_jardinagem'
    ),
    path(
        'concluir-servico-jardinagem/<str:userid>/<str:id_random>/<str:type>',
        concluir_servico_jardinagem,
        name='concluir_servico_jardinagem'
    ),
]