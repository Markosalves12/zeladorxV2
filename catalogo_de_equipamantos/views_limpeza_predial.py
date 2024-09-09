from django.shortcuts import reverse
from utils.views import generic_view, edit_generic_view
from catalogo_de_equipamantos.models_limpeza_predial import CatalogoDeEquipamentosLimpezaPredial
from catalogo_de_equipamantos.forms_limpeza_predial import CatalogoEquipamentoFormsLimpezaPredial

# Create your views here.
def catalogo_de_equipamentos_limpeza_predial(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Catálogo de equipamentos', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('catalogo_de_equipamentos_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('catalogo_de_equipamentos_limpeza_predial', kwargs={'userid': userid})},
    ]

    return generic_view(
        request=request,
        model=CatalogoDeEquipamentosLimpezaPredial,
        form_class=CatalogoEquipamentoFormsLimpezaPredial,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_equipamento_catalogo_jardinagem',
        app_name='catálogo de equipamentos',
        text_button_open_modal='Adicionar novo equipamento',
        text_button_save='Salvar equipamento',
        header_model='Novo equipamento',
        redirect_url='editar_equipamento_catalogo_limpeza_predial',
        link_tipos=tipos
    )

def editar_equipamento_catalogo_limpeza_predial(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=CatalogoDeEquipamentosLimpezaPredial,
        form_class=CatalogoEquipamentoFormsLimpezaPredial,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar equipamento do catálogo',
        redirect_url_name='editar_equipamento_catalogo_limpeza_predial',
        redirect_close_button='catalogo_de_equipamentos_limpeza_predial'
    )