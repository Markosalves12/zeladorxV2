from django.shortcuts import render, get_object_or_404
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem
from permissionscontrol.forms_jardinagem import PermissionsAccessJardinagemForms

# Create your views here.
def permissoes_jardinagem(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Gerente', 'label': 'Nome'},
        {'nome': 'Permissions', 'label': 'Permissões'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=PermissionsAccessJardinagem,
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_jardinagem',
        app_name='Permissões jardinagem',
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url='permissoes_jardinagem',
    )


def editar_permissoes_jardinagem(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessJardinagem,
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar permissoes',
        redirect_url_name='editar_permissoes_jardinagem',
        redirect_close_button='permissoes_jardinagem',
    )