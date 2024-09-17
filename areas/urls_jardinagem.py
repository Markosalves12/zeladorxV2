from django.urls import path
from areas.views_areas_jardinagem import areas_jardins, editar_area_jardins, areas_associadas_localidades_jardinagem

urlpatterns = [
    path('areas_jardins/<str:userid>', areas_jardins, name='areas_jardins'),
    path('editar_area_jardins/<str:userid>/<str:id_random>', editar_area_jardins, name='editar_area_jardins'),
    path('areas_associadas_localidades_jardinagem/<str:userid>/<str:id_random>', areas_associadas_localidades_jardinagem,
         name='areas_associadas_localidades_jardinagem'),
]