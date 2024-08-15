from django.shortcuts import render, redirect
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.forms import EmpresaSecundariaForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def empresas(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'razao_social', 'label': 'Razão social'},
        {'nome': 'CNPJ', 'label': 'CNPJ'},
        {'nome': 'setor', 'label': 'Setor'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=EmpresaSecundaria,
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_empresa',
        app_name='Empresas',
        text_button_open_modal='Adicionar nova empresa',
        text_button_save='Salvar empresa',
        header_model='Nova empresa',
        redirect_url='empresas'
    )

def editar_empresa(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=EmpresaSecundaria,
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar empresa',
        redirect_url_name='editar_empresa',
        redirect_close_button='empresas',
    )