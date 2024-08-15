from django.urls import path
from servicos.views_jardinagem import (agendar_servico, editar_servico_agendado, servicos_agendados,
                                       realizar_servico_agendado, cancelar_servico, concluir_servico)

urlpatterns = [
    path('agendar_servico', agendar_servico, name='agendar_servico'),
    path('editar_servico_agendado/<str:id_random>', editar_servico_agendado, name='editar_servico_agendado'),
    path('servicos_agendados', servicos_agendados, name='servicos_agendados'),
    path('realizar_servico_agendado/<str:id_random>', realizar_servico_agendado, name='realizar_servico_agendado'),
    path('cancelar_servico/<str:id_random>', cancelar_servico, name='cancelar_servico'),
    path('concluir_servico/<str:id_random>', concluir_servico, name='concluir_servico'),
]