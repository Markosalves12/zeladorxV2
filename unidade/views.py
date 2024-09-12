from django.shortcuts import render
from unidade.models import Unidade
from unidade.forms import UnidadeForms
from utils.views import generic_view, edit_generic_view
from empresasecundario.utils import define_empresas

# Create your views here.
def unidades(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'linkmapa', 'label': 'Mapa'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Mapa'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=Unidade.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria_id_random__in=empresas_secundarias_ids
        ),
        form_class=UnidadeForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_unidade',
        history_rout='visualizar_unidade',
        app_name='Unidades',
        text_button_open_modal='Adicionar nova unidade',
        text_button_save='Salvar unidade',
        header_model='Nova unidade',
        redirect_url='unidades',
        userid=userid
    )

def editar_unidade(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=Unidade,
        form_class=UnidadeForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar unidade',
        redirect_close_button='unidades',
        redirect_url_name='editar_unidade'
    )

def visualizar_unidade(request, id_random):
    objeto = Unidade.objects.get(
        id_random=id_random
    )

    return render(
        request=request,
        template_name="VisualizationMaps/VisualizationMaps.html",
        context={
            'app_name': f'Unidade {objeto.nome}',
            'objeto': objeto,
        }
    )