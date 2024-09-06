from django.shortcuts import reverse
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms
from utils.views import generic_view, edit_generic_view
from localidade.models_Jardinagem import LocalidadeJardiangem

# Create your views here.
def areas_jardins(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'Terreno', 'label': 'Terreno'},
        {'nome': 'vegetacao', 'label': 'vegetação'},
        {'nome': 'servico', 'label': 'Serviços'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('areas_jardins', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('areas_limpeza_predial', kwargs={'userid': userid})},
    ]

    return generic_view(
        request=request,
        model=AreasJardins,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        history_rout='historico_de_servicos_areas_jardinagem',
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


def areas_associadas_localidades_jardinagem(request, id_random):
    localidade = LocalidadeJardiangem.objects.get(
        id_random=id_random
    )

    objects = AreasJardins.objects.filter(
        localidade__id_random=id_random
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'Terreno', 'label': 'Terreno'},
        {'nome': 'vegetacao', 'label': 'vegetação'},
        {'nome': 'servico', 'label': 'Serviços'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('areas_jardins')},
        {'nome': 'Limpeza predial', 'link': reverse('areas_limpeza_predial')}
    ]

    return generic_view(
        request=request,
        model=objects,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        history_rout='historico_de_servicos_areas_jardinagem',
        app_name=f'Áreas Jardinagem - {localidade.nome}',
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url='areas_jardins',
        link_tipos=tipos
    )

