from django.urls import path
from areas.views_areas_jardinagem import areas_jardins, editar_area_jardins

urlpatterns = [
    path('areas_jardins', areas_jardins, name='areas_jardins'),
    path('editar_area_jardins/<str:id_random>', editar_area_jardins, name='editar_area_jardins'),
]