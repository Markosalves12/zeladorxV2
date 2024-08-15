from django.urls import path
from catalogo_de_servicos.views_jardinagem import catalogo_de_servicos_jardinagem, editar_catalogo_de_servicos_jardinagem
from catalogo_de_servicos.views_limpeza_predial import catalogo_de_servicos_limpeza_predial, editar_catalogo_de_servicos_limpeza_predial

urlpatterns = [
    # rota na raiz do sistema
    path('catalogo_de_servicos_jardinagem', catalogo_de_servicos_jardinagem, name='catalogo_de_servicos_jardinagem'),
    path('editar_catalogo_de_servicos_jardinagem/<str:id_random>', editar_catalogo_de_servicos_jardinagem, name='editar_catalogo_de_servicos_jardinagem'),

    path('catalogo_de_servicos_limpeza_predial', catalogo_de_servicos_limpeza_predial, name='catalogo_de_servicos_limpeza_predial'),
    path('editar_catalogo_de_servicos_limpeza_predial/<str:id_random>', editar_catalogo_de_servicos_limpeza_predial, name='editar_catalogo_de_servicos_limpeza_predial'),
]