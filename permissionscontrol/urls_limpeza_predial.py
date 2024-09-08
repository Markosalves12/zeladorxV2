from django.urls import path
from permissionscontrol.views_limpeza_predial import permissoes_limpeza_predial, editar_permissoes_limpeza_predial

urlpatterns = [
    path('permissoes_limpeza_predial/<str:userid>', permissoes_limpeza_predial, name='permissoes_limpeza_predial'),
    path('editar_permissoes_limpeza_predial/<str:userid>/<str:id_random>',
         editar_permissoes_limpeza_predial, name='editar_permissoes_limpeza_predial'),
]
