from django.shortcuts import render, reverse
from unidade.models import Unidade
from permissionscontrol.utils import validate_permissions


# Create your views here.
def visualizar_unidade_limpeza_predial(request, userid, id_random):
    objeto = Unidade.objects.get(
        id_random=id_random
    )

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['342: Pode visualizar unidades']
    )

    tipos = [
        {'nome': 'Tipo de mapa', 'link': ''},
        {
            'nome': 'Jardinagem',
            'link': reverse(
                'visualizar_unidade_jardinagem',
                kwargs={
                    'userid': userid,
                    'id_random': id_random
                }
            )
        },
        {
            'nome': 'Limpeza predial',
            'link': reverse(
                'visualizar_unidade_limpeza_predial',
                kwargs={
                    'userid': userid,
                    'id_random': id_random
                }
            )
        },
    ]

    return render(
        request=request,
        template_name="VisualizationMaps/VisualizationMaps.html",
        context={
            'app_name': f'Unidade {objeto.nome} - Mapa limpeza predial',
            'linkmapa': objeto.linkmapalimnpezapredial if objeto.linkmapalimnpezapredial else None,
            'objeto': objeto,
            'link_tipos': tipos,
            'permission_view': permission_view
        }
    )
