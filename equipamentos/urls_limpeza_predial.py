from django.urls import path
from equipamentos.views_limpeza_predial import (equipamentos_disponiveis_limpeza_predial,
                                                editar_equipamentos_disponiveis_limpeza_predial)


urlpatterns = [
    # rota na raiz do sistema
    path('equipamentos_disponiveis_limpeza_predial/<str:userid>', equipamentos_disponiveis_limpeza_predial,
         name='equipamentos_disponiveis_limpeza_predial'),
    path('editar_equipamentos_disponiveis_limpeza_predial/<str:userid>/<str:id_random>',
         editar_equipamentos_disponiveis_limpeza_predial, name='editar_equipamentos_disponiveis_limpeza_predial'),
]