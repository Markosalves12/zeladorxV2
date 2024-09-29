from django.shortcuts import render, reverse
from dashboards.data_visualization_limpeza_predial import (data_visualization_limpeza_predial_indicadores,
                                                           data_visualization_limpeza_predial_graphs)

# Create your views here.
def dashboard_produtividade_limpeza_predial(request, userid):
    (em_andamento, atrasados, proximos, agendamentos,
     total_de_areas_agendadas, total_de_areas_atrasadas,
     total_de_areas_proximas, total_de_areas_em_andamento) = data_visualization_limpeza_predial_indicadores(request, userid)

    fig_terreno = data_visualization_limpeza_predial_graphs(request, userid)

    tipos = [
        {'nome': 'Dashboards', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('dashboard_produtividade_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('dashboard_produtividade_limpeza_predial', kwargs={'userid': userid})},
    ]

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
            **fig_terreno,
        }
    )