from django.shortcuts import render, redirect
from equipamentos.models import EquipamentoDisponiveis
from equipamentos.forms import EquipamentoDisponivelForm
from utils.views import generic_view, edit_generic_view

# Create your views here.
def equipamentos_disponiveis(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Nome', 'label': 'Nome'},
        {'nome': 'DataDeAquisicao', 'label': 'Data de aquisição'},
        {'nome': 'matricula', 'label': 'Matricula'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=EquipamentoDisponiveis,
        form_class=EquipamentoDisponivelForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_equipamentos_disponiveis',
        app_name='equipamentos disponíveis',
        text_button_open_modal='Adicionar novo equipamento',
        text_button_save='Salvar equipamento',
        header_model='Novo equipamento',
        redirect_url='equipamentos_disponiveis'
    )


def editar_equipamentos_disponiveis(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=EquipamentoDisponiveis,
        form_class=EquipamentoDisponivelForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar equipamento disponível',
        redirect_url_name='editar_equipamentos_disponiveis',
        redirect_close_button='equipamentos_disponiveis',
    )