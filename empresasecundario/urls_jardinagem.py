from django.urls import path
from empresasecundario.views_jardinagem import empresas_jardinagem, editar_empresa_jardinagem

urlpatterns = [
    path('empresas_jardinagem/<str:userid>', empresas_jardinagem, name='empresas_jardinagem'),
    path('editar_empresa_jardinagem/<str:userid>/<str:id_random>/', editar_empresa_jardinagem, name='editar_empresa_jardinagem')
]