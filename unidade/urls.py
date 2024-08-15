from django.urls import path
from unidade.views import unidades, editar_unidade


urlpatterns = [
    # rota na raiz do sistema
    path('unidades', unidades, name='unidades'),
    path('editar_unidade/<str:id_random>', editar_unidade, name='editar_unidade'),
]