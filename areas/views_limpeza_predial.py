from django.shortcuts import reverse
from areas.models_limpeza_predial import AreaLimpezaPredial
from areas.forms_limpeza_predial import AreasLimpezaPredialForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def areas_limpeza_predial(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'dimensao', 'label': 'Dimensão'},
        {'nome': 'servico', 'label': 'Serviço'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('areas_jardins')},
        {'nome': 'Limpeza predial', 'link': reverse('areas_limpeza_predial')}
    ]

    return generic_view(
        request=request,
        model=AreaLimpezaPredial,
        form_class=AreasLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_limpeza_predial',
        app_name='Áreas Limpeza Predial',
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url='areas_limpeza_predial',
        link_tipos=tipos
    )

def editar_area_limpeza_predial(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=AreaLimpezaPredial,
        form_class=AreasLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar área limpeza predial',
        redirect_url_name='editar_area_limpeza_predial',
        redirect_close_button='areas_limpeza_predial'
    )