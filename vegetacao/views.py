from django.shortcuts import reverse
from vegetacao.models import CatalogoVegetacao
from vegetacao.forms import CatalogoVegetacaoForm
from utils.views import generic_view, edit_generic_view, gerneric_alter_status
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def vegetacao(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['352: Pode visualizar vegetações']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['351: Pode editar vegetações']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['350: Pode criar novas vegetações']
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
        model=CatalogoVegetacao.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
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
        permission_crate=permission_crate,
        userid=userid
    )


def editar_vegetacao(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['351: Pode editar vegetações']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['354: Pode desmobilizar vegetações']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['355: Pode reabilitar vegetações']
    )

    return edit_generic_view(
        request=request,
        model_class=CatalogoVegetacao,
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar vegetação',
        redirect_close_button=reverse('vegetacao', kwargs={'userid': userid}),
        redirect_url_name='editar_vegetacao',
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_vegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_vegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
    )

def alterar_status_vegetacao(request, userid, id_random, new_status):
    return gerneric_alter_status(
        request=request,
        model_class=CatalogoVegetacao,
        redirect_url_name=reverse(
            'editar_vegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        id_random=id_random,
        new_status=new_status
    )