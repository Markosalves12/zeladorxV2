from django.urls import path
from empresasecundario.views import empresas, editar_empresa

urlpatterns = [
    path('empresas/<str:userid>', empresas, name='empresas'),
    path('editar_empresa/<str:id_random>/', editar_empresa, name='editar_empresa')
]