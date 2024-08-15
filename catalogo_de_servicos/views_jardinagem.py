from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from catalogo_de_servicos.forms_jardinagem import CatalogoServicoJardinagemForms
from utils.views import generic_view, edit_generic_view


# Create your views here.
def catalogo_de_servicos_jardinagem(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=CatalogodeServicoJardinagem,
        form_class=CatalogoServicoJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_de_servicos_jardinagem',
        app_name='catálogo de serviços Jardinagem',
        text_button_open_modal='Adicionar novo serviço',
        text_button_save='Salvar serviço',
        header_model='Novo serviço',
        redirect_url='catalogo_de_servicos_jardinagem'
    )


def editar_catalogo_de_servicos_jardinagem(request, id_random):
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