# Create your views here.
from django.shortcuts import reverse
from gerente.models import Gerente
from gerente.forms_jardinagem import GerenteJardinagemForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def gerentes_jardinagem(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['282: Pode visualizar colaboradores']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['281: Pode editar colaboradores']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['280: Pode criar novos colaboradores']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'empresasecundaria', 'label': 'Empresa(s)'},
    ]

    tipos = [
        {'nome': 'Gerentes', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('gerentes_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('gerentes_limpeza_predial', kwargs={'userid': userid})},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=Gerente.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids,
            empresasecundaria__setor__setor='Jardinagem'
        ),
        form_class=GerenteJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_gerente_jardinagem',
        app_name='gerentes jardinagem',
        text_button_open_modal='Adicionar novo gerente',
        text_button_save='Salvar gerente',
        header_model='Novo gerente',
        redirect_url='gerentes_jardinagem',
        link_tipos=tipos,
        configurate_gerente=True,
        userid=userid,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_gerente_jardinagem(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['281: Pode editar colaboradores']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['283: Pode excluir colaboradores']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['284: Pode desmobilizar colaboradores']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['285: Pode reabilitar colaboradores']
    )

    return edit_generic_view(
        request=request,
        model_class=Gerente,
        form_class=GerenteJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar gerente',
        redirect_url_name='editar_gerente_jardinagem',
        redirect_close_button=reverse('gerentes_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_gerente_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_gerente_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )

def alterar_status_gerente_jardinagem(request, userid, id_random, new_status):
    return gerneric_alter_status(
        request=request,
        model_class=Gerente,
        redirect_url_name=reverse('editar_gerente_jardinagem', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status
    )