from django.urls import path
from gerente.views_limpeza_predial import gerentes_limpeza_predial, editar_gerente_limpeza_predial


urlpatterns = [
    # rota na raiz do sistema
    path('gerentes_limpeza_predial/<str:userid>', gerentes_limpeza_predial, name='gerentes_limpeza_predial'),
    path('editar_gerente_limpeza_predial/<str:userid>/<str:id_random>', editar_gerente_limpeza_predial, name='editar_gerente_limpeza_predial'),
]