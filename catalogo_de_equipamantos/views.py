from django.shortcuts import render, redirect
from utils.views import generic_view, edit_generic_view
from catalogo_de_equipamantos.models import CatalogoDeEquipamentos
from catalogo_de_equipamantos.forms import CatalogoEquipamentoForms

# Create your views here.
def catalogo_de_equipamentos(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=CatalogoDeEquipamentos,
        form_class=CatalogoEquipamentoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_equipamento_catalogo',
        app_name='catálogo de equipamentos',
        text_button_open_modal='Adicionar novo equipamento',
        text_button_save='Salvar equipamento',
        header_model='Novo equipamento',
        redirect_url='catalogo_de_equipamentos'
    )

def editar_equipamento_catalogo(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=CatalogoDeEquipamentos,
        form_class=CatalogoEquipamentoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar equipamento do catálogo',
        redirect_url_name='editar_equipamento_catalogo',
        redirect_close_button='catalogo_de_equipamentos'
    )