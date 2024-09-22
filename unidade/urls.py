from django.urls import path
from unidade.views import unidades, editar_unidade, visualizar_unidade, alterar_status_unidade


urlpatterns = [
    # rota na raiz do sistema
    path('unidades/<str:userid>', unidades, name='unidades'),
    path('editar_unidade/<str:userid>/<str:id_random>', editar_unidade, name='editar_unidade'),
    path('visualizar_unidade/<str:userid>/<str:id_random>', visualizar_unidade, name='visualizar_unidade'),
    path(
        'alterar_status_unidade/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_unidade,
        name='alterar_status_unidade'
    ),
]