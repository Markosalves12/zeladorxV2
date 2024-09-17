from django.shortcuts import reverse
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import (PermissionsAccessEspecials, PermissionsAccessJardinagem,
                                       PermissionsAccessLimpezaPredial)
from permissionscontrol.forms_especials import PermissionsAccessEspecialForms
from gerente.models import Gerente
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

def permissions_especials(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['301: Pode visualizar permissões especiais']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['300: Pode editar permissões especiais']
    )

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
        {'nome': 'Especiais', 'link': reverse('permissions_especials', kwargs={'userid': userid})},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=PermissionsAccessEspecials.objects.filter(
            Gerente__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Gerente__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=PermissionsAccessEspecialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_especials',
        app_name='Permissões especiais',
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url='permissions_especials',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        userid=userid
    )

def editar_permissoes_especials(request, userid, id_random):
    permissions_instance_especials = PermissionsAccessEspecials.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_jardinagem = PermissionsAccessJardinagem.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_limpeza_predial = PermissionsAccessLimpezaPredial.objects.filter(
        Gerente__id_random=userid
    ).first()

    gerente = Gerente.objects.get(
        id_random=userid
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['300: Pode editar permissões especiais']
    )

    tipos = [
        {'nome': 'Editar permissões', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('editar_permissoes_jardinagem',
                                               kwargs={'userid': userid, 'id_random': permissions_instance_jardinagem.id_random})},
        {'nome': 'Limpeza predial', 'link': reverse('editar_permissoes_limpeza_predial',
                                                     kwargs={'userid': userid, 'id_random': permissions_instance_limpeza_predial.id_random})},
        {'nome': 'Especiais', 'link': reverse('editar_permissoes_especials', kwargs={'userid': userid, 'id_random': permissions_instance_especials.id_random})},
    ]

    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessEspecials,
        form_class=PermissionsAccessEspecialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Editar permissoes especiais {gerente.username}',
        redirect_url_name='editar_permissoes_especials',
        redirect_close_button=reverse('permissions_especials', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_edit=permission_edit,
    )