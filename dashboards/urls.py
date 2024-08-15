from django.urls import path
from dashboards.views import dashboard_produtividade


urlpatterns = [
    # rota na raiz do sistema
    path('dashboard_produtividade', dashboard_produtividade, name='dashboard_produtividade'),
]