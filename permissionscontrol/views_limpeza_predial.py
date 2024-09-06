from django.shortcuts import render, get_object_or_404, reverse
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import PermissionsAccessLimpezaPredial, PermissionsLimpezaPredial
from permissionscontrol.forms_limpeza_predial import PermissionsAccessLimpezaPredialForms

# Create your views here.
def permissoes_limpeza_predial(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Gerente', 'label': 'Nome'},
        {'nome': 'Permissions', 'label': 'Permissões'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Tipo de permissão', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('permissoes_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('permissoes_limpeza_predial', kwargs={'userid': userid})},
    ]

    return generic_view(
        request=request,
        model=PermissionsAccessLimpezaPredial,
        form_class=PermissionsAccessLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_limpeza_predial',
        app_name='Permissões limpeza predial',
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url='permissoes_limpeza_predial',
        link_tipos=tipos
    )


def editar_permissoes_limpeza_predial(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessLimpezaPredial,
        form_class=PermissionsAccessLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar permissoes',
        redirect_url_name='editar_permissoes_limpeza_predial',
        redirect_close_button='permissoes_limpeza_predial',
    )