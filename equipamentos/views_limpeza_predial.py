from django.shortcuts import reverse
from equipamentos.models_limpeza_predial import EquipamentoDisponiveisLimpezaPredial
from equipamentos.forms_limpeza_predial import EquipamentoDisponivelLimpezaPredialForm
from utils.views import generic_view, edit_generic_view

# Create your views here.
def equipamentos_disponiveis_limpeza_predial(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Nome', 'label': 'Nome'},
        {'nome': 'DataDeAquisicao', 'label': 'Data de aquisição'},
        {'nome': 'matricula', 'label': 'Matricula'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Equipamentos disponiveis', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('equipamentos_disponiveis_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('equipamentos_disponiveis_limpeza_predial', kwargs={'userid': userid})},
    ]

    return generic_view(
        request=request,
        model=EquipamentoDisponiveisLimpezaPredial,
        form_class=EquipamentoDisponivelLimpezaPredialForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_equipamentos_disponiveis_limpeza_predial',
        app_name='equipamentos disponíveis limpeza predial',
        text_button_open_modal='Adicionar novo equipamento',
        text_button_save='Salvar equipamento',
        header_model='Novo equipamento',
        redirect_url='equipamentos_disponiveis_limpeza_predial',
        link_tipos=tipos
    )


def editar_equipamentos_disponiveis_limpeza_predial(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=EquipamentoDisponiveisLimpezaPredial,
        form_class=EquipamentoDisponivelLimpezaPredialForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar equipamento disponível',
        redirect_url_name='editar_equipamentos_disponiveis_limpeza_predial',
        redirect_close_button='equipamentos_disponiveis_limpeza_predial',
    )