from django.urls import path
from terrenos.views import terrenos, editar_terreno

urlpatterns = [
    path('terrenos', terrenos, name='terrenos'),
    path('editar_terreno/<str:id_random>', editar_terreno, name='editar_terreno'),
]