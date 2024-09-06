from django.shortcuts import reverse
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from localidade.forms_limpeza_predial import LocalidadeLimpezaPredialForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def localidades_limpeza_predial(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'lat_med', 'label': 'Lat. média'},
        {'nome': 'long_med', 'label': 'Long. média'},
        {'nome': 'unidade', 'label': 'unidade'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Áreas associadas'},
    ]

    tipos = [
        {'nome': 'Tipo de localidade', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('localidades_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('localidades_limpeza_predial', kwargs={'userid': userid})},
    ]

    return generic_view(
        request=request,
        model=LocalidadeLimpezaPredial,
        form_class=LocalidadeLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_localidade_limpeza_predial',
        history_rout='areas_associadas_localidades_limpeza_predial',
        app_name='localidades limpeza predial',
        text_button_open_modal='Adicionar nova localidade',
        text_button_save='Salvar localidade',
        header_model='Nova localidade',
        redirect_url='localidades_limpeza_predial',
        link_tipos=tipos
    )


def editar_localidade_limpeza_predial(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=LocalidadeLimpezaPredial,
        form_class=LocalidadeLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar localidade',
        redirect_url_name='editar_localidade_limpeza_predial',
        redirect_close_button='localidades_limpeza_predial',
    )