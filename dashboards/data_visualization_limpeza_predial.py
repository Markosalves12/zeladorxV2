from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from django.db.models.functions import Now
from django.db.models import F, Q, ExpressionWrapper, IntegerField
from django.utils import timezone
from datetime import timedelta
from dashboards.data_visualization import calculate_areas_and_counts, generate_chart, generate_grouped_chart
from dashboards.utils_limpeza_predial import colect_dados_jardinagem

def data_visualization_limpeza_predial_indicadores(request, userid):
    agendado = colect_dados_jardinagem(
        request=request,
        userid=userid
    )

    em_andamento = agendado.filter(status='Em andamento').count()
    atrasados = agendado.filter(DataDeInicio__lt=timezone.now().date()).exclude(status="Em andamento").count()

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    proximos = agendado.filter(
        DataDeInicio__gte=one_day,
        DataDeInicio__lte=seven_days
    ).exclude(
        status="Em andamento",
        DataDeInicio__lte=seven_days
    ).count()

    agendamentos = agendado.filter(
        status='Agendado',
        DataDeInicio__gte=seven_days,
    ).count()

    total_de_areas_agendadas = calculate_areas_and_counts(agendado, 'Agendado', Q(DataDeInicio__gte=seven_days))
    total_de_areas_atrasadas = calculate_areas_and_counts(agendado, 'Agendado',
                                                          Q(DataDeInicio__lt=timezone.now().date()))
    total_de_areas_proximas = calculate_areas_and_counts(agendado, 'Agendado',
                                                         Q(DataDeInicio__gte=one_day) & Q(DataDeInicio__lte=seven_days))
    total_de_areas_em_andamento = calculate_areas_and_counts(agendado, 'Em andamento')

    return (em_andamento, atrasados, proximos, agendamentos, total_de_areas_agendadas,
            total_de_areas_atrasadas, total_de_areas_proximas, total_de_areas_em_andamento)


def data_visualization_limpeza_predial_graphs(request, userid):
    agendado = colect_dados_jardinagem(
        request=request,
        userid=userid
    )

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    fig_charts = {
        # Localidade
        'fig_area_localidade_atrasado': generate_chart(
            agendado.filter(
                DataDeInicio__lt=timezone.now().date()
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (Atrasados)',
            label_type='Localidade',
            color='#dc3444'
        ).to_html(full_html=True),

        'fig_area_localidade_proximo': generate_chart(
            agendado.filter(
                DataDeInicio__gte=one_day,
                DataDeInicio__lte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (Próximos)',
            label_type='Localidade',
            color='#f6be04'
        ).to_html(full_html=False),

        'fig_area_localidade_agendados': generate_chart(
            agendado.filter(
                DataDeInicio__gte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (agendados)',
            label_type='Localidade',
            color='#14a0b6'
        ).to_html(full_html=False),

        'fig_area_localidade_em_andamento': generate_chart(
            agendado,
            status='Em andamento',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (em andamento)',
            label_type='Localidade',
            color='#2aa042'
        ).to_html(full_html=False),

        # Areas
        'fig_area_area_atrasado': generate_chart(
            agendado.filter(
                DataDeInicio__lt=timezone.now().date()
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (Atrasados)',
            label_type='Área',
            color='#dc3444'
        ).to_html(full_html=True),

        'fig_area_area_proximo': generate_chart(
            agendado.filter(
                DataDeInicio__gte=one_day,
                DataDeInicio__lte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (Próximos)',
            label_type='Área',
            color='#f6be04'
        ).to_html(full_html=False),

        'fig_area_area_agendados': generate_chart(
            agendado.filter(
                DataDeInicio__gte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (agendados)',
            label_type='Área',
            color='#14a0b6'
        ).to_html(full_html=False),

        'fig_area_area_em_andamento': generate_chart(
            agendado,
            status='Em andamento',
            field_name='Areas__nome',
            title='Área Total por área limpeza predial (em andamento)',
            label_type='Área',
            color='#2aa042'
        ).to_html(full_html=False),

        # mes a mes
        'fig_mes_html': generate_grouped_chart(
            agendado,
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Serviços por Mês/vegetação (Agendado)',
            label_type='localidade'
        ).to_html(full_html=False),
    }

    return fig_charts


def data_visualization_limpeza_predial_reports(request, userid):
    agendado = colect_dados_jardinagem(
        request=request,
        userid=userid
    )

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    fig_charts = {
        # Localidade
        'fig_area_localidade_atrasado': generate_chart(
            agendado.filter(
                DataDeInicio__lt=timezone.now().date()
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (Atrasados)',
            label_type='Localidade',
            color='#dc3444'
        ),

        'fig_area_localidade_proximo': generate_chart(
            agendado.filter(
                DataDeInicio__gte=one_day,
                DataDeInicio__lte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (Próximos)',
            label_type='Localidade',
            color='#f6be04'
        ),

        'fig_area_localidade_agendados': generate_chart(
            agendado.filter(
                DataDeInicio__gte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (agendados)',
            label_type='Localidade',
            color='#14a0b6'
        ),

        'fig_area_localidade_em_andamento': generate_chart(
            agendado,
            status='Em andamento',
            field_name='Areas__localidade__nome',
            title='Área Total por localidade (em andamento)',
            label_type='Localidade',
            color='#2aa042'
        ),

        # Areas
        'fig_area_area_atrasado': generate_chart(
            agendado.filter(
                DataDeInicio__lt=timezone.now().date()
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (Atrasados)',
            label_type='Área',
            color='#dc3444'
        ),

        'fig_area_area_proximo': generate_chart(
            agendado.filter(
                DataDeInicio__gte=one_day,
                DataDeInicio__lte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (Próximos)',
            label_type='Área',
            color='#f6be04'
        ),

        'fig_area_area_agendados': generate_chart(
            agendado.filter(
                DataDeInicio__gte=seven_days,
            ),
            status='Agendado',
            field_name='Areas__nome',
            title='Área Total por área verde (agendados)',
            label_type='Área',
            color='#14a0b6'
        ),

        'fig_area_area_em_andamento': generate_chart(
            agendado,
            status='Em andamento',
            field_name='Areas__nome',
            title='Área Total por área limpeza predial (em andamento)',
            label_type='Área',
            color='#2aa042'
        ),

        # mes a mes
        'fig_mes_html': generate_grouped_chart(
            agendado,
            status='Agendado',
            field_name='Areas__localidade__nome',
            title='Serviços por Mês/vegetação (Agendado)',
            label_type='localidade'
        ),
    }

    return fig_charts

