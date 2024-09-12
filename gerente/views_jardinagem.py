# Create your views here.
from django.shortcuts import reverse
from gerente.models import Gerente
from gerente.forms import GerenteForms
from utils.views import generic_view, edit_generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def gerentes_jardinagem(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['272: Pode visualizar colaboradores']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['271: Pode editar colaboradores']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['270: Pode criar novos colaboradores']
    )

    colunas = [
        {'nome': 'id','label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa(s)'},
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
            empresasecundaria__id_random__in=empresas_secundarias_ids
        ),
        form_class=GerenteForms,
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
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_gerente_jardinagem(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=Gerente,
        form_class=GerenteForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar gerente',
        redirect_url_name='editar_gerente_jardinagem',
        redirect_close_button='gerentes_jardinagem',
    )
