from django.urls import path
from authenticate.views import login, logout, reset_password, update_password


urlpatterns = [
    # rota na raiz do sistema
    path('', login, name='login'),
    path('reset_password', reset_password, name='reset_password'),
    path('update_password/<str:token>', update_password, name='update_password'),
    path('logout', logout, name='logout'),
]
