from django.urls import path
from vegetacao.views import vegetacao, editar_vegetacao, alterar_status_vegetacao, areas_associadas_vegetacao

urlpatterns = [
    path('vegetacao/<str:userid>', vegetacao, name='vegetacao'),
    path('editar_vegetacao/<str:userid>/<str:id_random>', editar_vegetacao, name='editar_vegetacao'),
    path(
        'alterar_status_vegetacao/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_vegetacao,
        name='alterar_status_vegetacao'
    ),
    path(
        'areas_associadas_vegetacao/<str:userid>/<str:id_random>',
        areas_associadas_vegetacao,
        name='areas_associadas_vegetacao'
    ),
]