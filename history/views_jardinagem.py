from django.shortcuts import render, reverse
from areas.models_jardinagem import AreasJardins
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.utils import paginate
from utils.utils import aplicar_filtros_dinamicos

# Create your views here.
def historico_de_servicos_areas_jardinagem(request, userid, id_random):
    objeto = AreasJardins.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        Areas__id_random=id_random,
        status__in=['Concluido']
    )

    filtro_mapeamento = {
        'TipoServico': 'TipoServico',
        'ServicosEscalados': 'ServicosEscalados',
        'ColaboradoresEscalados': 'ColaboradoresEscalados',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    get_data = {
        'DataDeInicio': 'None',
        'DataDeConclusao': 'None',
        'ServicosEscalados': 'None',
        'ColaboradoresEscalados': 'None',
        'Areas': 'None',
        'TipoServico': 'None',
    }

    if request.method == 'GET':
        get_data = request.GET.dict()
        objetos = aplicar_filtros_dinamicos(objetos, get_data, filtro_mapeamento)
        get_multiple_data = request.GET

        get_data = {
            'DataDeInicio': ', '.join(get_multiple_data.getlist(
                'DataDeInicio')) if 'DataDeInicio' in get_multiple_data and get_multiple_data.getlist(
                'DataDeInicio') and get_multiple_data.getlist('DataDeInicio')[0] != '' else 'None',
            'DataDeConclusao': ', '.join(get_multiple_data.getlist(
                'DataDeConclusao')) if 'DataDeConclusao' in get_multiple_data and get_multiple_data.getlist(
                'DataDeConclusao') and get_multiple_data.getlist('DataDeConclusao')[0] != '' else 'None',
            'ServicosEscalados': ', '.join(get_multiple_data.getlist(
                'ServicosEscalados')) if 'ServicosEscalados' in get_multiple_data and get_multiple_data.getlist(
                'ServicosEscalados') else 'None',
            'ColaboradoresEscalados': ', '.join(get_multiple_data.getlist(
                'ColaboradoresEscalados')) if 'ColaboradoresEscalados' in get_multiple_data and get_multiple_data.getlist(
                'ColaboradoresEscalados') else 'None',
            'Areas': ', '.join(
                get_multiple_data.getlist('Areas')) if 'Areas' in get_multiple_data and get_multiple_data.getlist(
                'Areas') and get_multiple_data.getlist('Areas')[0] != '' else 'None',
            'TipoServico': ', '.join(get_multiple_data.getlist(
                'TipoServico')) if 'TipoServico' in get_multiple_data and get_multiple_data.getlist(
                'TipoServico') and get_multiple_data.getlist('TipoServico')[0] != '' else 'None',
        }

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=2
    )

    return render(
        request=request,
        template_name="history/history.html",
        context={
            'app_name': f'Histórico de serviços {objeto.nome}',
            'objeto': objeto,
            'foto_objeto': objeto.foto.url if objeto.foto else None,
            'Foto': True,
            'type': 'jardinagem_agendado',
            'form_search': ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': 'areas'
                }
            ),
            'export_excel': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': 'areas',
                }
            ),
        }
    )

def historico_de_servicos_catologo_de_servicos_jardinagem(request, userid, id_random):
    objeto = CatalogodeServicoJardinagem.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        ServicosEscalados__id_random=id_random,
        status__in=['Concluido']
    )

    filtro_mapeamento = {
        'Areas': 'Areas__id',
        'TipoServico': 'TipoServico',
        'ColaboradoresEscalados': 'ColaboradoresEscalados',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    if request.method == 'GET':
        get_data = request.GET.dict()
        objetos = aplicar_filtros_dinamicos(objetos, get_data, filtro_mapeamento)

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=2
    )

    return render(
        request=request,
        template_name="history/history.html",
        context={
            'app_name': f'Histórico de serviços {objeto.nome}',
            'objeto': objeto,
            'foto_objeto': None,
            'Foto': False,
            'type': 'jardinagem_agendado',
            'form_search': ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                'exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'catalogo_de_servicos',
                }
            ),
            'export_excel': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'catalogo_de_servicos',
                }
            ),
        }
    )