from django.urls import path
from gerente.views import gerentes, editar_gerente


urlpatterns = [
    # rota na raiz do sistema
    path('gerentes/<str:userid>', gerentes, name='gerentes'),
    path('editar_gerente/<str:id_random>', editar_gerente, name='editar_gerente'),
]