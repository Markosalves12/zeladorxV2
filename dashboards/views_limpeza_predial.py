from django.shortcuts import render, reverse, redirect
from dashboards.data_visualization_limpeza_predial import data_visualization_limpeza_predial_indicadores
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from utils.utils import aplicar_filtros_dinamicos
from dashboards.utils_limpeza_predial import colect_dados_limpeza_predial
from dashboards.utils_limpeza_predial import graphs_limpeza_predial_to_html
from empresasecundario.utils import define_empresas

# Create your views here.
def dashboard_produtividade_limpeza_predial(request, userid):
    agendado = colect_dados_limpeza_predial(
        request=request,
        userid=userid
    )

    filtro_mapeamento = {
        'Areas': 'Areas__id',
        'TipoServico': 'TipoServico',
        'ServicosEscalados': 'ServicosEscalados__id',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Dashboards', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('dashboard_produtividade_jardinagem', kwargs={'userid': userid})},)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('dashboard_produtividade_limpeza_predial', kwargs={'userid': userid})},)


    if request.method == 'GET':
        get_data = request.GET.dict()
        agendado = aplicar_filtros_dinamicos(agendado, get_data, filtro_mapeamento)

    (em_andamento, atrasados, proximos, agendamentos) = data_visualization_limpeza_predial_indicadores(request, userid, agendado)

    (fig_area_area_atrasado, fig_area_localidade_atrasado, fig_area_localidade_proximo,
     fig_area_area_proximo, fig_area_localidade_agendados, fig_area_area_agendados,
     fig_area_localidade_em_andamento, fig_area_area_em_andamento, fig_mes_html) = graphs_limpeza_predial_to_html(request, userid, agendado)

    return render(
        request=request,
        template_name='dashboards/dashboard_produtividade.html',
        context={
            'app_name': 'Dashboard gerencial limpeza predial',
            'link_tipos': tipos,
            'agendamentos': agendamentos,
            'proximos': proximos,
            'atrasados': atrasados,
            'em_andamento': em_andamento,
            'por_terreno': False,
            'por_colaborador': False,
            'form_search': ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            **fig_area_area_atrasado,
            **fig_area_localidade_atrasado,
            **fig_area_localidade_proximo,
            **fig_area_area_proximo,
            **fig_area_localidade_agendados,
            **fig_area_area_agendados,
            **fig_area_localidade_em_andamento,
            **fig_area_area_em_andamento,
            **fig_mes_html
        }
    )