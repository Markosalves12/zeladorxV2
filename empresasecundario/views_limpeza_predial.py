from django.shortcuts import reverse
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.forms import EmpresaSecundariaForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions

# Create your views here.
def empresas_limpeza_predial(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['272: Pode visualizar empresas']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['271: Pode editar empresas']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['270: Pode criar novas empresas']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'razao_social', 'label': 'Razão social'},
        {'nome': 'CNPJ', 'label': 'CNPJ'},
        {'nome': 'setor', 'label': 'Setor'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Tipo de empresa', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('empresas_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('empresas_limpeza_predial', kwargs={'userid': userid})}
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    return generic_view(
        request=request,
        model=EmpresaSecundaria.objects.filter(
            empresaprimaria__id_random__in=empresas_primarias_ids,
            setor__setor__in=['Limpeza predial']
        ),
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_empresa_limpeza_predial',
        app_name='Empresas limpeza predial',
        form_search=EmpresaSecundariaForms(request=request, userid=userid, type='search'),
        sform_search=False,
        filtro_mapeamento={
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova empresa',
        text_button_save='Salvar empresa',
        header_model='Nova empresa',
        redirect_url='empresas_limpeza_predial',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_empresa_limpeza_predial(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['271: Pode editar empresas']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['273: Pode excluir empresas']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['274: Pode desmobilizar empresas']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['275: Pode reabilitar empresas']
    )

    return edit_generic_view(
        request=request,
        model_class=EmpresaSecundaria,
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar empresa',
        redirect_url_name='editar_empresa_limpeza_predial',
        redirect_close_button=reverse('empresas_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_rehabilitate=permission_rehabilitate,
        permission_desmobilize=permission_desmobilize,
        url_desmobilize=reverse(
            'alterar_status_empresa_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_empresa_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )

def alterar_status_empresa_limpeza_predial(request, userid, id_random, new_status):
    objeto = EmpresaSecundaria.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=EmpresaSecundaria,
        redirect_url_name=reverse('editar_empresa_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )