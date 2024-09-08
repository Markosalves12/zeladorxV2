from django.shortcuts import reverse
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms
from utils.views import generic_view, edit_generic_view
from localidade.models_Jardinagem import LocalidadeJardiangem
from permissionscontrol.utils import validate_permissions
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def areas_jardins(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['252: Pode visualizar áreas de jardinagem']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['250: Pode criar novas áreas de jardinagem']
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
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_area_jardins(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    return edit_generic_view(
        request=request,
        model_class=AreasJardins,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar área Jardins',
        redirect_url_name='editar_area_jardins',
        redirect_close_button='areas_jardins',
        permission_edit=permission_edit
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

