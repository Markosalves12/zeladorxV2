from django.db.models import Q
from django.utils import timezone
from dashboards.data_visualization import calculate_areas_and_counts, generate_chart, generate_grouped_chart
from dashboards.utils_limpeza_predial import colect_dados_limpeza_predial
from utils.utils import define_range_time

def data_visualization_limpeza_predial_indicadores(request, userid, agendado):
    em_andamento = agendado.filter(status='Em andamento').count()
    atrasados = agendado.filter(DataDeInicio__lt=timezone.now().date()).exclude(status="Em andamento").count()

    one_day, seven_days = define_range_time()

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



class data_visualization_limpeza_predial_graphs:
    def __init__(self, request, userid, agendado):
        self.request = request
        self.userid = userid
        self.agendados = agendado

    one_day, seven_days = define_range_time()

    def define_figs_atrasados(self):
        fig_charts = {
            # Localidade
            'fig_area_localidade_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Atrasados)',
                label_type='Localidade',
                color='#dc3444'
            ).to_html(full_html=True),

            # Areas
            'fig_area_area_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (Atrasados)',
                label_type='Área',
                color='#dc3444'
            ).to_html(full_html=True),
        }

        return fig_charts

    def define_figs_proximos(self):
        fig_charts = {
            'fig_area_localidade_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Próximos)',
                label_type='Localidade',
                color='#f6be04'
            ).to_html(full_html=False),

            'fig_area_area_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (Próximos)',
                label_type='Área',
                color='#f6be04'
            ).to_html(full_html=False),
        }

        return fig_charts

    def define_figs_agendados(self):
        fig_charts = {
            'fig_area_localidade_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (agendados)',
                label_type='Localidade',
                color='#14a0b6'
            ).to_html(full_html=False),

            'fig_area_area_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (agendados)',
                label_type='Área',
                color='#14a0b6'
            ).to_html(full_html=False),
        }

        return fig_charts

    def define_figs_em_andamento(self):
        fig_charts = {
            'fig_area_localidade_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (em andamento)',
                label_type='Localidade',
                color='#2aa042'
            ).to_html(full_html=False),

            'fig_area_area_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__nome',
                title='Área Total por área limpeza predial (em andamento)',
                label_type='Área',
                color='#2aa042'
            ).to_html(full_html=False),
        }

        return fig_charts

    def define_figs_by_months(self):
        fig_charts = {
            # mes a mes
            'fig_mes_html': generate_grouped_chart(
                self.agendados,
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Serviços por Mês/vegetação (Agendado)',
                label_type='localidade'
            ).to_html(full_html=False),
        }

        return fig_charts

class data_visualization_limpeza_predial_reports:
    def __init__(self, request, userid):
        self.request = request
        self.userid = userid
        self.agendados = self.get_data()

    def get_data(self):
        agendado = colect_dados_limpeza_predial(
            request=self.request,
            userid=self.userid
        )

        return agendado

    one_day, seven_days = define_range_time()

    def define_figs_atrasados(self):
        fig_charts = {
            # Localidade
            'fig_area_localidade_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Atrasados)',
                label_type='Localidade',
                color='#dc3444'
            ),

            # Areas
            'fig_area_area_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (Atrasados)',
                label_type='Área',
                color='#dc3444'
            ),
        }

        return fig_charts

    def define_figs_proximos(self):
        fig_charts = {
            'fig_area_localidade_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Próximos)',
                label_type='Localidade',
                color='#f6be04'
            ),

            'fig_area_area_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (Próximos)',
                label_type='Área',
                color='#f6be04'
            ),
        }

        return fig_charts

    def define_figs_agendados(self):
        fig_charts = {
            'fig_area_localidade_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (agendados)',
                label_type='Localidade',
                color='#14a0b6'
            ),

            'fig_area_area_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__nome',
                title='Área Total por área verde (agendados)',
                label_type='Área',
                color='#14a0b6'
            ),
        }

        return fig_charts

    def define_figs_em_andamento(self):
        fig_charts = {
            'fig_area_localidade_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (em andamento)',
                label_type='Localidade',
                color='#2aa042'
            ),

            'fig_area_area_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__nome',
                title='Área Total por área limpeza predial (em andamento)',
                label_type='Área',
                color='#2aa042'
            ),
        }

        return fig_charts

    def define_figs_concluidos(self):
        fig_charts = {
            'fig_area_localidade_concluidos': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Concluidos)',
                label_type='Localidade',
                color='#Concluidos'
            ),

            'fig_area_area_concluidos': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='Areas__nome',
                title='Área Total por área limpeza predial (Concluidos)',
                label_type='Área',
                color='#Concluidos'
            ),
        }

        return fig_charts

    def define_figs_by_months(self):
        fig_charts = {
            # mes a mes
            'fig_mes_html': generate_grouped_chart(
                self.agendados,
                status='Agendado',
                field_name='Areas__localidade__nome',
                title='Serviços por Mês/vegetação (Agendado)',
                label_type='localidade'
            ),
        }

        return fig_charts

