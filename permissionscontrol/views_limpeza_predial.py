from django.shortcuts import reverse
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import PermissionsAccessLimpezaPredial, PermissionsAccessJardinagem
from permissionscontrol.forms_limpeza_predial import PermissionsAccessLimpezaPredialForms
from gerente.models import Gerente

# Create your views here.
def permissoes_limpeza_predial(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Gerente','label': 'Nome'},
        { 'nome': 'Permissions','label': 'Permissões' },
        {'nome': 'acoes','label': 'Ações'},
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
        link_tipos=tipos,
        userid=userid
    )


# o envio do id random esta quebrando o codigo
# definir o id random dentro da função
def editar_permissoes_limpeza_predial(request, userid, id_random):
    permissions_instance = PermissionsAccessJardinagem.objects.filter(
        Gerente__id_random=userid
    ).first()
    gerente = Gerente.objects.get(
        id_random=userid
    )

    tipos = [
        {'nome': 'Editar permissões', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('editar_permissoes_jardinagem',kwargs={
            'userid': userid, 'id_random': permissions_instance.id_random})},
        {'nome': 'Limpeza predial', 'link': reverse('editar_permissoes_limpeza_predial',
                                                   kwargs={'userid': userid, 'id_random': id_random})},
    ]

    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessLimpezaPredial,
        form_class=PermissionsAccessLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Editar permissoes limpeza predia {gerente.username}',
        redirect_url_name='editar_permissoes_limpeza_predial',
        redirect_close_button='permissoes_limpeza_predial',
        link_tipos=tipos
    )