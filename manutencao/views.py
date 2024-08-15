from django.shortcuts import render, redirect
from manutencao.models import CatalogoManutencao, MotivoDaManutencao, ManutencaoDeEquipamentos
from manutencao.forms import CatalogoManutencaoForms, MotivoDaManutencaoForms, ManutencaoDeEquipamentosForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def catalogo_manutencao(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=CatalogoManutencao,
        form_class=CatalogoManutencaoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_manutencao',
        app_name='Catálogo de manutenção',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='catalogo_manutencao'
    )

def editar_catalogo_manutencao(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=CatalogoManutencao,
        form_class=CatalogoManutencaoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar manutencao do catálogo',
        redirect_url_name='editar_catalogo_manutencao',
        redirect_close_button='catalogo_manutencao',
    )


def catalogo_motivos(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=MotivoDaManutencao,
        form_class=MotivoDaManutencaoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_catalogo_motivos',
        palavra_chave='Catálogo de motivos',
        redirect_url='catalogo_motivos'
    )


def editar_catalogo_motivos(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=MotivoDaManutencao,
        form_class=MotivoDaManutencaoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar motivo do catálogo',
        redirect_url_name='editar_catalogo_motivos',
        redirect_close_button='catalogo_motivos'
    )


def manutencao_de_equipametos(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Equipamento', 'label': 'Equipamento'},
        {'nome': 'DataDeInicio', 'label': 'Data de envio'},
        {'nome': 'DataFim', 'label': 'Data de retorno'},
        {'nome': 'CatalogoManutencao', 'label': 'Tipo de manutencao'},
        {'nome': 'MotivoManutencao', 'label': 'Motivo'},
        {'nome': 'Descricaodoservico', 'label': 'Descrição'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=ManutencaoDeEquipamentos,
        form_class=ManutencaoDeEquipamentosForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_manutencao_de_equipametos',
        palavra_chave='Manutenção de equipamentos',
        redirect_url='manutencao_de_equipametos'
    )

def editar_manutencao_de_equipametos(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=ManutencaoDeEquipamentos,
        form_class=ManutencaoDeEquipamentosForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar manutencão',
        redirect_url_name='editar_manutencao_de_equipametos',
        redirect_close_button='manutencao_de_equipametos',
    )