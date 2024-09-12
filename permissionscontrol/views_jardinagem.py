from django.shortcuts import reverse
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsAccessLimpezaPredial
from permissionscontrol.forms_jardinagem import PermissionsAccessJardinagemForms
from gerente.models import Gerente
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def permissoes_jardinagem(request, userid):
    # permission_view = validate_permissions(
    #     request=request,
    #     userid=userid,
    #     permission_type='jardinagem',
    #     permission_to_access=['256: Pode visualizar localidades',]
    # )
    #
    # permission_edit = validate_permissions(
    #     request=request,
    #     userid=userid,
    #     permission_type='jardinagem',
    #     permission_to_access=['255: Pode editar localidades']
    # )
    #
    # permission_crate = validate_permissions(
    #     request=request,
    #     userid=userid,
    #     permission_type='jardinagem',
    #     permission_to_access=['254: Pode criar novas localidades',]
    # )

    colunas = [
        {'nome': 'id','label': '#','largura': '10px'},
        {'nome': 'Gerente', 'label': 'Nome'},
        {'nome': 'Permissions','label': 'Permissões'},
        {'nome': 'acoes','label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Tipo de permissão', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('permissoes_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('permissoes_limpeza_predial', kwargs={'userid': userid})},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=PermissionsAccessJardinagem.objects.filter(
            Gerente__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Gerente__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_jardinagem',
        app_name='Permissões jardinagem',
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url='permissoes_jardinagem',
        link_tipos=tipos,
        # permission_view=permission_view,
        # permission_edit=permission_edit,
        # permission_crate=permission_crate
        userid=userid
    )


def editar_permissoes_jardinagem(request, userid, id_random):
    permissions_instance = PermissionsAccessLimpezaPredial.objects.filter(
        Gerente__id_random=userid
    ).first()
    gerente = Gerente.objects.get(
        id_random=userid
    )

    tipos = [
        {'nome': 'Editar permissões', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('editar_permissoes_jardinagem',
                                               kwargs={'userid': userid, 'id_random': id_random})},
        {'nome': 'Limpeza predial', 'link': reverse('editar_permissoes_limpeza_predial',
                                                     kwargs={'userid': userid,'id_random': permissions_instance.id_random})},
    ]

    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessJardinagem,
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Editar permissoes jardinagem {gerente.username}',
        redirect_url_name='editar_permissoes_jardinagem',
        redirect_close_button='permissoes_jardinagem',
        link_tipos=tipos,
    )