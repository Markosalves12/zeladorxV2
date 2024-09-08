from django.urls import path
from localidade.views_limpeza_predial import localidades_limpeza_predial, editar_localidade_limpeza_predial


urlpatterns = [
    path('localidades_limpeza_predial/<str:userid>', localidades_limpeza_predial, name='localidades_limpeza_predial'),
    path('editar_localidade_limpeza_predial/<str:userid>/<str:id_random>', editar_localidade_limpeza_predial,name='editar_localidade_limpeza_predial'),
]