from django.urls import path
from calendario.views import calendario, tabeladedados

urlpatterns = [
    path('calendario', calendario, name='calendario'),
    path('tabeladedados', tabeladedados, name='tabeladedados')
]