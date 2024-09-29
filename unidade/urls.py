from django.urls import path
from unidade.views import unidades, editar_unidade, alterar_status_unidade
from unidade.maps_jardinagem import visualizar_unidade_jardinagem
from unidade.maps_limpeza_predial import visualizar_unidade_limpeza_predial


urlpatterns = [
    # rota na raiz do sistema
    path('unidades/<str:userid>', unidades, name='unidades'),
    path('editar_unidade/<str:userid>/<str:id_random>', editar_unidade, name='editar_unidade'),
    path('visualizar_unidade_jardinagem/<str:userid>/<str:id_random>',
         visualizar_unidade_jardinagem, name='visualizar_unidade_jardinagem'),
    path('visualizar_unidade_limpeza_predial/<str:userid>/<str:id_random>',
         visualizar_unidade_limpeza_predial, name='visualizar_unidade_limpeza_predial'),
    path(
        'alterar_status_unidade/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_unidade,
        name='alterar_status_unidade'
    ),
]