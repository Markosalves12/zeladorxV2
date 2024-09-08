from django.urls import path
from catalogo_de_equipamantos.views import catalogo_de_equipamentos, editar_equipamento_catalogo


urlpatterns = [
    # rota na raiz do sistema
    path('catalogo_de_equipamentos/<str:userid>', catalogo_de_equipamentos, name='catalogo_de_equipamentos'),
    path('editar_equipamento_catalogo/<str:userid>/<str:id_random>', editar_equipamento_catalogo, name='editar_equipamento_catalogo'),
]