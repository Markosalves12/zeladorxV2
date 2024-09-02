from django.urls import path
from permissionscontrol.views import permissoes_jardinagem, editar_permissoes_jardinagem

urlpatterns = [
    path('permissoes_jardinagem', permissoes_jardinagem, name='permissoes_jardinagem'),
    path('editar_permissoes_jardinagem/<str:id_random>', editar_permissoes_jardinagem, name='editar_permissoes_jardinagem'),
]

