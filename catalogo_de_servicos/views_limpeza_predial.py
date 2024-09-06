from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from catalogo_de_servicos.forms_limpeza_predial import CatalogoServicoLimpezaPredialForms
from utils.views import generic_view, edit_generic_view
from django.shortcuts import reverse


# Create your views here.
def catalogo_de_servicos_limpeza_predial(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    tipos = [
        {'nome': 'Catálogo de serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('catalogo_de_servicos_jardinagem')},
        {'nome': 'Limpeza predial', 'link': reverse('catalogo_de_servicos_limpeza_predial')}
    ]

    return generic_view(
        request=request,
        model=CatalogodeServicoLimpezaPredial,
        form_class=CatalogoServicoLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_de_servicos_limpeza_predial',
        history_rout='historico_de_servicos_catologo_de_servicos_limpeza_predial',
        app_name='catálogo de serviços limpeza predial',
        text_button_open_modal='Adicionar novo serviço',
        text_button_save='Salvar serviço',
        header_model='Novo serviço',
        redirect_url='catalogo_de_servicos_limpeza_predial',
        link_tipos=tipos
    )

def editar_catalogo_de_servicos_limpeza_predial(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=CatalogodeServicoLimpezaPredial,
        form_class=CatalogoServicoLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço do catálogo de limpeza predial',
        redirect_url_name='editar_catalogo_de_servicos_limpeza_predial',
        redirect_close_button='catalogo_de_servicos_limpeza_predial'
    )