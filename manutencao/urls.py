from django.urls import path
from manutencao.views import (catalogo_manutencao, editar_catalogo_manutencao, catalogo_motivos,
                              editar_catalogo_motivos, manutencao_de_equipametos, editar_manutencao_de_equipametos)

urlpatterns = [
    path('catalogo_manutencao', catalogo_manutencao, name='catalogo_manutencao'),
    path('editar_catalogo_manutencao/<str:id_random>', editar_catalogo_manutencao, name='editar_catalogo_manutencao'),

    path('catalogo_motivos', catalogo_motivos, name='catalogo_motivos'),
    path('editar_catalogo_motivos/<str:id_random>', editar_catalogo_motivos, name='editar_catalogo_motivos'),

    path('manutencao_de_equipametos', manutencao_de_equipametos, name='manutencao_de_equipametos'),
    path('editar_manutencao_de_equipametos/<str:id_random>', editar_manutencao_de_equipametos, name='editar_manutencao_de_equipametos'),
]