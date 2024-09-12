from django.shortcuts import render, redirect
from terrenos.models import Terreno
from terrenos.forms import TerrenoForms
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def terrenos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['260: Pode visualizar terrenos']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['259: Pode editar terrenos']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['258: Pode criar novos terrenos']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=Terreno.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids
        ),
        form_class=TerrenoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_terreno',
        app_name='Terrenos',
        text_button_open_modal='Adicionar novo terreno',
        text_button_save='Salvar terreno',
        header_model='Novo terreno',
        redirect_url='terrenos',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_terreno(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['259: Pode editar terrenos']
    )

    return edit_generic_view(
        request=request,
        model_class=Terreno,
        form_class=TerrenoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar terreno',
        redirect_close_button='terrenos',
        redirect_url_name='editar_terreno',
        permission_edit=permission_edit
    )