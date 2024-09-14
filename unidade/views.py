from django.shortcuts import render
from unidade.models import Unidade
from unidade.forms import UnidadeForms
from utils.views import generic_view, edit_generic_view
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions

# Create your views here.
def unidades(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['342: Pode visualizar unidades']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['341: Pode editar unidades']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['340: Pode criar novas unidades']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'linkmapa', 'label': 'Mapa'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Mapa'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=Unidade.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids
        ),
        form_class=UnidadeForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_unidade',
        history_rout='visualizar_unidade',
        app_name='Unidades',
        text_button_open_modal='Adicionar nova unidade',
        text_button_save='Salvar unidade',
        header_model='Nova unidade',
        redirect_url='unidades',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )

def editar_unidade(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['341: Pode editar unidades']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['343: Pode excluir unidades']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['344: Pode desmobilizar unidades']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['345: Pode reabilitar unidades']
    )

    return edit_generic_view(
        request=request,
        model_class=Unidade,
        form_class=UnidadeForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar unidade',
        redirect_close_button='unidades',
        redirect_url_name='editar_unidade',
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate
    )

def visualizar_unidade(request, userid,id_random):
    objeto = Unidade.objects.get(
        id_random=id_random
    )

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['342: Pode visualizar unidades']
    )

    return render(
        request=request,
        template_name="VisualizationMaps/VisualizationMaps.html",
        context={
            'app_name': f'Unidade {objeto.nome}',
            'objeto': objeto,
            'permission_view': permission_view
        }
    )