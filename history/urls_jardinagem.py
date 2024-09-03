from django.urls import path
from gestor.views import gestores, editar_gestor


urlpatterns = [
    # rota na raiz do sistema
    path('gestores', gestores, name='gestores'),
    path('editar_gestor/<str:id_random>', editar_gestor, name='editar_gestor'),
]