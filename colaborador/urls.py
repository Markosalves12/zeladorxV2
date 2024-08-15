from django.urls import path
from colaborador.views import colaboradores, editar_colaborador


urlpatterns = [
    # rota na raiz do sistema
    path('colaboradores', colaboradores, name='colaboradores'),
    path('editar_colaborador/<str:id_random>', editar_colaborador, name='editar_colaborador'),
]
