from django.urls import path
from authenticate.views import login, logout


urlpatterns = [
    # rota na raiz do sistema
    path('', login, name='login'),
    path('logout', logout, name='logout'),
]
