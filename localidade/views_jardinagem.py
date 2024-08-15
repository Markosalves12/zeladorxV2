from django.shortcuts import reverse
from localidade.models_Jardinagem import LocalidadeJardiangem
from localidade.forms_jardinagem import LocalidadeJardinagemForms
from utils.views import generic_view, edit_generic_view

# Create your views here.
def localidades_jardinagem(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'lat_med', 'label': 'Lat. média'},
        {'nome': 'long_med', 'label': 'Long. média'},
        {'nome': 'unidade', 'label': 'unidade'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    tipos = [
        {'nome': 'Tipo de localidade', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('localidades_jardinagem')},
        {'nome': 'Limpeza predial', 'link': reverse('localidades_limpeza_predial')},
        # {'nome': 'Controle de pragas', 'link': ''},
        # {'nome': 'Limpeza urbana', 'link': ''},
    ]

    return generic_view(
        request=request,
        model=LocalidadeJardiangem,
        form_class=LocalidadeJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_localidade_jardinagem',
        app_name='localidades jardinagem',
        text_button_open_modal='Adicionar nova localidade',
        text_button_save='Salvar localidade',
        header_model='Nova localidade',
        redirect_url='localidades_jardinagem',
        link_tipos=tipos
    )


def editar_localidade_jardinagem(request, id_random):
    return edit_generic_view(
        request=request,
        model_class=LocalidadeJardiangem,
        form_class=LocalidadeJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar localidade',
        redirect_url_name='editar_localidade_jardinagem',
        redirect_close_button='localidades_jardinagem',
    )