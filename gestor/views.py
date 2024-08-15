from django.shortcuts import render, redirect
from gestor.models import Gestor
from gestor.forms import GestorForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def gestores(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'E-mail'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
    ]

    return generic_view(
        request=request,
        model=Gestor,
        form_class=GestorForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_gestor',
        app_name='gestores',
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar gestor',
        header_model='Novo gestor',
        redirect_url='gestores'
    )


def editar_gestor(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=Gestor,
        form_class=GestorForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar gestor',
        redirect_url_name='editar_gestor',
        redirect_close_button='gestores',
    )

