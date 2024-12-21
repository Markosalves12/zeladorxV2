from django.urls import path
from dashboards.views_jardinagem import dashboard_produtividade_jardinagem


urlpatterns = [
    # rota na raiz do sistema
    path(
        'dashboard-gerencial-jardinagem/<userid>',
        dashboard_produtividade_jardinagem,
        name='dashboard_produtividade_jardinagem'
    ),
]