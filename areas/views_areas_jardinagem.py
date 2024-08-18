from django.shortcuts import reverse
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def areas_jardins(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'Terreno', 'label': 'Terreno'},
        {'nome': 'vegetacao', 'label': 'vegetação'},
        {'nome': 'servico', 'label': 'Serviços'},
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
        model=AreasJardins,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        app_name='Áreas Jardinagem',
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url='areas_jardins',
        link_tipos=tipos
    )

def editar_area_jardins(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=AreasJardins,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar área Jardins',
        redirect_url_name='editar_area_jardins',
        redirect_close_button='areas_jardins'
    )