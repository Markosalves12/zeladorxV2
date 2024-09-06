from django.urls import path
from vegetacao.views import vegetacao, editar_vegetacao

urlpatterns = [
    path('vegetacao/<str:userid>', vegetacao, name='vegetacao'),
    path('editar_vegetacao/<str:id_random>', editar_vegetacao, name='editar_vegetacao'),
]