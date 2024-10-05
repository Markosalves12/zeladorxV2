from django.shortcuts import reverse
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from localidade.forms_limpeza_predial import LocalidadeLimpezaPredialForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def localidades_limpeza_predial(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['292: Pode visualizar localidades']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['291: Pode editar localidades']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['290: Pode criar novas localidades']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome','label': 'Nome'},
        {'nome': 'lat_med', 'label': 'Lat. média'},
        {'nome': 'long_med','label': 'Long. média'},
        {'nome': 'unidade','label': 'unidade'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Áreas associadas'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de localidade', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('localidades_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('localidades_limpeza_predial', kwargs={'userid': userid})})

    return generic_view(
        request=request,
        model=LocalidadeLimpezaPredial.objects.filter(
            unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ),
        form_class=LocalidadeLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_localidade_limpeza_predial',
        history_rout='areas_associadas_localidades_limpeza_predial',
        app_name='localidades limpeza predial',
        form_search=LocalidadeLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'unidade': 'unidade__id',
            'nome': 'nome',
        },
        text_button_open_modal='Adicionar nova localidade',
        text_button_save='Salvar localidade',
        header_model='Nova localidade',
        redirect_url='localidades_limpeza_predial',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_localidade_limpeza_predial(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['291: Pode editar localidades']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['293: Pode excluir localidades']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['294: Pode desmobilizar localidades']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['295: Pode reabilitar localidades']
    )

    return edit_generic_view(
        request=request,
        model_class=LocalidadeLimpezaPredial,
        form_class=LocalidadeLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar localidade',
        redirect_url_name='editar_localidade_limpeza_predial',
        redirect_close_button=reverse('localidades_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_localidade_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_localidade_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )

def alterar_status_localidade_limpeza_predial(request, userid, id_random, new_status):
    objeto = LocalidadeLimpezaPredial.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=LocalidadeLimpezaPredial,
        redirect_url_name=reverse(
            'editar_localidade_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        id_random=id_random,
        new_status=new_status,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )