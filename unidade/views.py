from django.shortcuts import render, redirect
from unidade.models import Unidade
from unidade.forms import UnidadeForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def unidades(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'linkmapa', 'label': 'Mapa'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=Unidade,
        form_class=UnidadeForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_unidade',
        app_name='Unidades',
        text_button_open_modal='Adicionar nova unidade',
        text_button_save='Salvar unidade',
        header_model='Nova unidade',
        redirect_url='unidades'
    )

def editar_unidade(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=Unidade,
        form_class=UnidadeForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar unidade',
        redirect_close_button='unidades',
        redirect_url_name='editar_unidade'
    )

