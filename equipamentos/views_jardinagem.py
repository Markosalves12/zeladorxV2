from django.shortcuts import reverse
from equipamentos.models_jardinagem import EquipamentoDisponiveisJardinagem
from equipamentos.forms_jardinagem import EquipamentoDisponivelJardinagemForm
from utils.views import generic_view, edit_generic_view

# Create your views here.
def equipamentos_disponiveis_jardinagem(request, userid):
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
        model=EquipamentoDisponiveisJardinagem,
        form_class=EquipamentoDisponivelJardinagemForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_equipamentos_disponiveis_jardinagem',
        app_name='equipamentos disponíveis jardinagem',
        text_button_open_modal='Adicionar novo equipamento',
        text_button_save='Salvar equipamento',
        header_model='Novo equipamento',
        redirect_url='equipamentos_disponiveis_jardinagem',
        link_tipos=tipos
    )


def editar_equipamentos_disponiveis_jardinagem(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=EquipamentoDisponiveisJardinagem,
        form_class=EquipamentoDisponivelJardinagemForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar equipamento disponível',
        redirect_url_name='editar_equipamentos_disponiveis_jardinagem',
        redirect_close_button='equipamentos_disponiveis_jardinagem',
    )