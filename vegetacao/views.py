from django.shortcuts import render, redirect
from vegetacao.models import CatalogoVegetacao
from vegetacao.forms import CatalogoVegetacaoForm
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresa_primaria_ids

# Create your views here.
def vegetacao(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['264: Pode visualizar vegetações']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['263: Pode editar vegetações']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['262: Pode criar novas vegetações']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)

    return generic_view(
        request=request,
        model=CatalogoVegetacao.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids
        ),
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_vegetacao',
        app_name='vegetação',
        text_button_open_modal='Adicionar nova vegetação',
        text_button_save='Salvar vegetação',
        header_model='Nova vegetação',
        redirect_url='vegetacao',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_vegetacao(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['263: Pode editar vegetações']
    )

    return edit_generic_view(
        request=request,
        model_class=CatalogoVegetacao,
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar vegetação',
        redirect_close_button='vegetacao',
        redirect_url_name='editar_vegetacao',
        permission_edit=permission_edit
    )