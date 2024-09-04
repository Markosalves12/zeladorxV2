from django.urls import path
from history.views_jardinagem import historico_de_servicos_areas_jardinagem


urlpatterns = [
    # rota na raiz do sistema
    path('historico_de_servicos_areas_jardinagem/<str:id_random>', historico_de_servicos_areas_jardinagem, name='historico_de_servicos_areas_jardinagem'),
]