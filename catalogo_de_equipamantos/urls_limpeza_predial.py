from django.urls import path
from catalogo_de_equipamantos.views_limpeza_predial import catalogo_de_equipamentos_limpeza_predial, editar_equipamento_catalogo_limpeza_predial


urlpatterns = [
    # rota na raiz do sistema
    path('catalogo_de_equipamentos_limpeza_predial/<str:userid>', catalogo_de_equipamentos_limpeza_predial, name='catalogo_de_equipamentos_limpeza_predial'),
    path('editar_equipamento_catalogo_limpeza_predial/<str:userid>/<str:id_random>', editar_equipamento_catalogo_limpeza_predial, name='editar_equipamento_catalogo_limpeza_predial'),
]