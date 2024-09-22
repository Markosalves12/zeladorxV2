from django.urls import path
from dashboards.views_limpeza_predial import dashboard_produtividade_limpeza_predial


urlpatterns = [
    # rota na raiz do sistema
    path(
        'dashboard_produtividade_limpeza_predial/<userid>',
         dashboard_produtividade_limpeza_predial,
         name='dashboard_produtividade_limpeza_predial'
    ),
]