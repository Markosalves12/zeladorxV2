from django.shortcuts import render, redirect
from colaborador.models import Colaborador
from colaborador.forms import ColaboradorForms
from utils.views import generic_view, edit_generic_view


# Create your views here.
def colaboradores(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'username', 'label': 'Nome'},
        {'nome': 'email', 'label': 'Email'},
        {'nome': 'atividades', 'label': 'atividades'},
        {'nome': 'gerente', 'label': 'gerentes'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=Colaborador,
        form_class=ColaboradorForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_colaborador',
        app_name='colaboradores',
        text_button_open_modal='Adicionar novo colaborador',
        text_button_save='Salvar colaborador',
        header_model='Novo colaborador',
        redirect_url='colaboradores',
    )


def editar_colaborador(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=Colaborador,
        form_class=ColaboradorForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar colaborador',
        redirect_url_name='editar_colaborador',
        redirect_close_button='colaboradores',
    )
