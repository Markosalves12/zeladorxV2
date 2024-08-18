from django.urls import path
from servicos.views_limpeza_predial import (agendar_servico_limpeza_predial, editar_servico_limpezapredial_agendado,
                                            realizar_servico_limpeza_predial_agendado, servicos_agendados_limpeza_predial)


urlpatterns = [
    path('agendar_servico_limpeza_predial', agendar_servico_limpeza_predial, name='agendar_servico_limpeza_predial'),
    path('editar_servico_limpezapredial_agendado/<str:id_random>', editar_servico_limpezapredial_agendado, name='editar_servico_limpezapredial_agendado'),
    path('servicos_agendados_limpeza_predial', servicos_agendados_limpeza_predial, name='servicos_agendados_limpeza_predial'),
    path('realizar_servico_limpeza_predial_agendado/<str:id_random>', realizar_servico_limpeza_predial_agendado, name='realizar_servico_limpeza_predial_agendado'),
]