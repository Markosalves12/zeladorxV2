from django.urls import path
from catalogo_de_materiais.views import materiais, categoria_material, consumo_material


urlpatterns = [
    # rota na raiz do sistema
    path('materiais', materiais, name='materiais'),
    path('categoria_material', categoria_material, name='categoria_material'),
    path('consumo_material', consumo_material, name='consumo_material'),
]
