from django.urls import path
from localidade.views_jardinagem import localidades_jardinagem, editar_localidade_jardinagem


urlpatterns = [
    path('localidades_jardinagem/<str:userid>', localidades_jardinagem, name='localidades_jardinagem'),
    path('editar_localidade_jardinagem/<str:userid>/<str:id_random>', editar_localidade_jardinagem, name='editar_localidade_jardinagem'),
]