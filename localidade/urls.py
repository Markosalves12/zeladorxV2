from django.urls import path
from localidade.views_jardinagem import localidades_jardinagem, editar_localidade_jardinagem
from localidade.views_limpeza_predial import localidades_limpeza_predial, editar_localidade_limpeza_predial


urlpatterns = [
    path('localidades_jardinagem', localidades_jardinagem, name='localidades_jardinagem'),
    path('editar_localidade_jardinagem/<str:id_random>', editar_localidade_jardinagem, name='editar_localidade_jardinagem'),
    path('localidades_limpeza_predial', localidades_limpeza_predial, name='localidades_limpeza_predial'),
    path('editar_localidade_limpeza_predial/<str:id_random>', editar_localidade_limpeza_predial,name='editar_localidade_limpeza_predial'),
]