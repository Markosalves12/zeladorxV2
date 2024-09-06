# Create your views here.
from django.shortcuts import render, redirect
from gerente.models import Gerente
from gerente.forms import GerenteForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def gerentes(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa(s)'},
    ]

    return generic_view(
        request=request,
        model=Gerente,
        form_class=GerenteForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_gerente',
        app_name='gerentes',
        text_button_open_modal='Adicionar novo gerente',
        text_button_save='Salvar gerente',
        header_model='Novo gerente',
        redirect_url='gerentes',
        configurate_gerente=True,
    )


def editar_gerente(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=Gerente,
        form_class=GerenteForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar gerente',
        redirect_url_name='editar_gerente',
        redirect_close_button='gerentes',
    )
