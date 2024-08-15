from django.urls import path
from equipamentos.views import equipamentos_disponiveis, editar_equipamentos_disponiveis


urlpatterns = [
    # rota na raiz do sistema
    path('equipamentos_disponiveis', equipamentos_disponiveis, name='equipamentos_disponiveis'),
    path('editar_equipamentos_disponiveis/<str:id_random>', editar_equipamentos_disponiveis, name='editar_equipamentos_disponiveis'),
]