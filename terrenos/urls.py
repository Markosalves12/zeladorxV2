from django.urls import path
from terrenos.views import terrenos, editar_terreno, alterar_status_terreno, areas_associadas_terrenos

urlpatterns = [
    path('terrenos/<str:userid>', terrenos, name='terrenos'),
    path('editar_terreno/<str:userid>/<str:id_random>', editar_terreno, name='editar_terreno'),
    path(
        'alterar_status_terreno/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_terreno,
        name='alterar_status_terreno'
    ),
    path(
        'areas_associadas_terrenos/<str:userid>/<str:id_random>',
        areas_associadas_terrenos,
        name='areas_associadas_terrenos'
    ),
]