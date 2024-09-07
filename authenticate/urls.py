from django.urls import path
from authenticate.views import login, logout, access_rejected


urlpatterns = [
    # rota na raiz do sistema
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('access_rejected/<str:userid>', access_rejected, name='access_rejected'),
]
