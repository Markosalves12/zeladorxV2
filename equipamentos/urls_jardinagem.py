from django.urls import path
from equipamentos.views_jardinagem import (equipamentos_disponiveis_jardinagem,
                                           editar_equipamentos_disponiveis_jardinagem)


urlpatterns = [
    # rota na raiz do sistema
    path('equipamentos_disponiveis_jardinagem/<str:userid>', equipamentos_disponiveis_jardinagem,
         name='equipamentos_disponiveis_jardinagem'),
    path('editar_equipamentos_disponiveis_jardinagem/<str:userid>/<str:id_random>',
         editar_equipamentos_disponiveis_jardinagem, name='editar_equipamentos_disponiveis_jardinagem'),
]