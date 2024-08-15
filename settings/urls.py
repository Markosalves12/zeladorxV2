from django.urls import path
from settings.views import (configuracoes_do_gestor, configuracoes_do_colaborador
                            # editar_configuracao_gestor
                            )


urlpatterns = [
    # rota na raiz do sistema
    path('configuracoes_do_gestor', configuracoes_do_gestor, name='configuracoes_do_gestor'),
    path('configuracoes_do_colaborador', configuracoes_do_colaborador, name='configuracoes_do_colaborador'),
    # path('editar_configuracao_gestor/<str:id_random>', editar_configuracao_gestor, name='editar_configuracao_gestor'),
]