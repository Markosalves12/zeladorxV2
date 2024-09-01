from django.urls import path
from servicos.views_limpeza_predial import (agendar_servico_limpeza_predial, servicos_agendados_limpeza_predial,
                                            editar_servico_limpeza_predial_agendado,
                                            configurar_servico_limpeza_predial, editar_servico_limpezapredial_configurado,
                                            realizar_servico_limpeza_predial_agendado, servicos_configurados_limpeza_predial)


urlpatterns = [
    path('agendar_servico_limpeza_predial', agendar_servico_limpeza_predial, name='agendar_servico_limpeza_predial'),
    path('servicos_agendados_limpeza_predial', servicos_agendados_limpeza_predial, name='servicos_agendados_limpeza_predial'),
    path('editar_servico_limpeza_predial_agendado/<str:id_random>', editar_servico_limpeza_predial_agendado, name='editar_servico_limpeza_predial_agendado'),
    path('configurar_servico_limpeza_predial', configurar_servico_limpeza_predial, name='configurar_servico_limpeza_predial'),
    path('editar_servico_limpezapredial_configurado/<str:id_random>', editar_servico_limpezapredial_configurado, name='editar_servico_limpezapredial_configurado'),
    path('servicos_configurados_limpeza_predial', servicos_configurados_limpeza_predial, name='servicos_configurados_limpeza_predial'),
    path('realizar_servico_limpeza_predial_agendado/<str:id_random>', realizar_servico_limpeza_predial_agendado, name='realizar_servico_limpeza_predial_agendado'),
]