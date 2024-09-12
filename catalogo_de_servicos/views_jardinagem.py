from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from catalogo_de_servicos.forms_jardinagem import CatalogoServicoJardinagemForms
from utils.views import generic_view, edit_generic_view
from django.shortcuts import reverse
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas


# Create your views here.
def catalogo_de_servicos_jardinagem(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['268: Pode visualizar serviços do catálogo']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['267: Pode editar serviços do catálogo']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['266: Pode criar novos serviços ao catálogo']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    tipos = [
        {'nome': 'Catálogo de serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('catalogo_de_servicos_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('catalogo_de_servicos_limpeza_predial', kwargs={'userid': userid})},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=CatalogodeServicoJardinagem.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids
        ),
        form_class=CatalogoServicoJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_de_servicos_jardinagem',
        history_rout='historico_de_servicos_catologo_de_servicos_jardinagem',
        app_name='catálogo de serviços Jardinagem',
        text_button_open_modal='Adicionar novo serviço',
        text_button_save='Salvar serviço',
        header_model='Novo serviço',
        redirect_url='catalogo_de_servicos_jardinagem',
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_catalogo_de_servicos_jardinagem(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=CatalogodeServicoJardinagem,
        form_class=CatalogoServicoJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço do catálogo de jardinagem',
        redirect_url_name='editar_catalogo_de_servicos_jardinagem',
        redirect_close_button='catalogo_de_servicos_jardinagem'
    )