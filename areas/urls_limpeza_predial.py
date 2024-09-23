from django.urls import path
from areas.views_limpeza_predial import (areas_limpeza_predial, editar_area_limpeza_predial,
                                         areas_associadas_localidades_limpeza_predial, alterar_status_areas_limpeza_predial)

urlpatterns = [
    path('areas_limpeza_predial/<str:userid>', areas_limpeza_predial, name='areas_limpeza_predial'),
    path('editar_area_limpeza_predial/<str:userid>/<str:id_random>', editar_area_limpeza_predial, name='editar_area_limpeza_predial'),
    path('areas_associadas_localidades_limpeza_predial/<str:userid>/<str:id_random>', areas_associadas_localidades_limpeza_predial,
         name='areas_associadas_localidades_limpeza_predial'),
    path('alterar_status_areas_limpeza_predial/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_areas_limpeza_predial,
         name='alterar_status_areas_limpeza_predial'
    ),
]