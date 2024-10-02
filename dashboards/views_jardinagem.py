from django.shortcuts import render, reverse
from dashboards.data_visualization_jardinagem import (data_visualization_jardinagem_indicadores,
                                                      data_visualization_jardinagem_graphs)
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.utils import aplicar_filtros_dinamicos
from dashboards.utils_jardinagem import colect_dados_jardinagem

# Create your views here.
def dashboard_produtividade_jardinagem(request, userid):
    agendado = colect_dados_jardinagem(
        request=request,
        userid=userid
    )

    filtro_mapeamento = {
        'Areas': 'Areas__id',
        'TipoServico': 'TipoServico',
        'ServicosEscalados': 'ServicosEscalados__id',
        'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    if request.method == 'GET':
        get_data = request.GET.dict()
        agendado = aplicar_filtros_dinamicos(agendado, get_data, filtro_mapeamento)

    (em_andamento, atrasados, proximos, agendamentos,
     total_de_areas_agendadas, total_de_areas_atrasadas,
     total_de_areas_proximas, total_de_areas_em_andamento) = data_visualization_jardinagem_indicadores(request, userid, agendado)

    figs_atrasados = data_visualization_jardinagem_graphs(request, userid, agendado).define_figs_atrasados()
    figs_proximos = data_visualization_jardinagem_graphs(request, userid, agendado).define_figs_proximos()
    figs_agendados = data_visualization_jardinagem_graphs(request, userid, agendado).define_figs_agendados()
    figs_em_andamento = data_visualization_jardinagem_graphs(request, userid, agendado).define_figs_em_andamento()
    figs_by_months = data_visualization_jardinagem_graphs(request, userid, agendado).define_figs_by_months()

    tipos = [
        {'nome': 'Dashboards', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('dashboard_produtividade_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('dashboard_produtividade_limpeza_predial', kwargs={'userid': userid})},
    ]

    return render(
        request=request,
        template_name='dashboards/dashboard_produtividade.html',
        context={
            'app_name': 'Dashboard gerencial jardinagem',
            'link_tipos': tipos,
            'agendamentos': agendamentos,
            'proximos': proximos,
            'atrasados': atrasados,
            'em_andamento': em_andamento,
            'por_terreno': True,
            'por_colaborador': True,
            'form_search': ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            **figs_atrasados,
            **figs_proximos,
            **figs_agendados,
            **figs_em_andamento,
            **figs_by_months,
        }
    )