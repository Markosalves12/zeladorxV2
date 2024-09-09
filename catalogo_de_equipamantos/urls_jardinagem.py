from django.urls import path
from catalogo_de_equipamantos.views_jardinagem import (catalogo_de_equipamentos_jardinagem,
                                                       editar_equipamento_catalogo_jardinagem)


urlpatterns = [
    # rota na raiz do sistema
    path('catalogo_de_equipamentos_jardinagem/<str:userid>', catalogo_de_equipamentos_jardinagem, name='catalogo_de_equipamentos_jardinagem'),
    path('editar_equipamento_catalogo_jardinagem/<str:userid>/<str:id_random>', editar_equipamento_catalogo_jardinagem, name='editar_equipamento_catalogo_jardinagem'),
]