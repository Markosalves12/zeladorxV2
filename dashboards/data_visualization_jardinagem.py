from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models.functions import Now
from django.db.models import F, Q, ExpressionWrapper, IntegerField
from django.utils import timezone
from datetime import timedelta
from dashboards.data_visualization import calculate_areas_and_counts, generate_chart, generate_grouped_chart
from dashboards.utils_jardinagem import colect_dados_jardinagem

def data_visualization_jardinagem_indicadores(request, userid, agendado):
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


class data_visualization_jardinagem_graphs:
    def __init__(self, request, userid, agendado):
        self.request = request
        self.userid = userid
        self.agendados = agendado

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    def define_figs_atrasados(self):
        fig_charts = {
            # Terrenos
            'fig_area_terreno_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (Atrasados)',
                label_type='Terreno',
                color='#dc3444'
            ).to_html(full_html=False),

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

            # Colaborador
            'fig_area_colaborador_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (Atrasados)',
                label_type='Colaborador',
                color='#dc3444'
            ).to_html(full_html=True),
        }

        return fig_charts

    def define_figs_proximos(self):
        fig_charts = {
            'fig_area_terreno_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (Próximos)',
                label_type='Terreno',
                color='#f6be04'
            ).to_html(full_html=False),

            # Localidade
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

            # Areas
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

            'fig_area_colaborador_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (Próximos)',
                label_type='Colaborador',
                color='#f6be04'
            ).to_html(full_html=False),

        }

        return fig_charts

    def define_figs_agendados(self):
        fig_charts = {
            'fig_area_terreno_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (agendados)',
                label_type='Terreno',
                color='#14a0b6'
            ).to_html(full_html=False),

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

            'fig_area_colaborador_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (agendados)',
                label_type='Colaborador',
                color='#14a0b6'
            ).to_html(full_html=False),
        }

        return fig_charts

    def define_figs_em_andamento(self):
        fig_charts = {
            'fig_area_terreno_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (em andamento)',
                label_type='Terreno',
                color='#2aa042'
            ).to_html(full_html=False),

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
                title='Área Total por área verde (em andamento)',
                label_type='Área',
                color='#2aa042'
            ).to_html(full_html=False),

            'fig_area_colaborador_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (em andamento)',
                label_type='Colaborador',
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
                field_name='Areas__vegetacao__nome',
                title='Serviços por Mês/vegetação (Agendado)',
                label_type='vegetação'
            ).to_html(full_html=False),
        }

        return fig_charts


class data_visualization_jardinagem_reports:
    def __init__(self, request, userid):
        self.request = request
        self.userid = userid
        self.agendados = self.get_data()

    def get_data(self):
        agendado = colect_dados_jardinagem(
            request=self.request,
            userid=self.userid
        )

        return agendado

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    def define_figs_atrasados(self):
        fig_charts = {
            # Terrenos
            'fig_area_terreno_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (Atrasados)',
                label_type='Terreno',
                color='#dc3444'
            ),

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

            # Colaborador
            'fig_area_colaborador_atrasado': generate_chart(
                self.agendados.filter(
                    DataDeInicio__lt=timezone.now().date()
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (Atrasados)',
                label_type='Colaborador',
                color='#dc3444'
            ),
        }

        return fig_charts

    def define_figs_proximos(self):
        fig_charts = {
            'fig_area_terreno_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (Próximos)',
                label_type='Terreno',
                color='#f6be04'
            ),

            # Localidade
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

            # Areas
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

            'fig_area_colaborador_proximo': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.one_day,
                    DataDeInicio__lte=self.seven_days,
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (Próximos)',
                label_type='Colaborador',
                color='#f6be04'
            ),

        }

        return fig_charts

    def define_figs_agendados(self):
        fig_charts = {
            'fig_area_terreno_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (agendados)',
                label_type='Terreno',
                color='#14a0b6'
            ),

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

            'fig_area_colaborador_agendados': generate_chart(
                self.agendados.filter(
                    DataDeInicio__gte=self.seven_days,
                ),
                status='Agendado',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (agendados)',
                label_type='Colaborador',
                color='#14a0b6'
            ),
        }

        return fig_charts

    def define_figs_em_andamento(self):
        fig_charts = {
            'fig_area_terreno_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (em andamento)',
                label_type='Terreno',
                color='#2aa042'
            ).to_html(full_html=False),

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
                title='Área Total por área verde (em andamento)',
                label_type='Área',
                color='#2aa042'
            ),

            'fig_area_colaborador_em_andamento': generate_chart(
                self.agendados,
                status='Em andamento',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (em andamento)',
                label_type='Colaborador',
                color='#2aa042'
            ),
        }

        return fig_charts

    def define_figs_concluidos(self):
        fig_charts = {
            # Terrenos
            'fig_area_terreno_concluido': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='Areas__Terreno__nome',
                title='Área Total por Tipo de Terreno (Atrasados)',
                label_type='Terreno',
                color='#add8e6'
            ),

            'fig_area_area_concluidos': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='Areas__nome',
                title='Área Total por área verde (Atrasados)',
                label_type='Área',
                color='#add8e6'
            ),

            'fig_area_localidade_concluidos': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='Areas__localidade__nome',
                title='Área Total por localidade (Atrasados)',
                label_type='Localidade',
                color='#add8e6'
            ),

            # Colaborador
            'fig_area_colaborador_concluidos': generate_chart(
                self.agendados,
                status='Concluido',
                field_name='ColaboradoresEscalados__username',
                title='Área Total por colaborador (Atrasados)',
                label_type='Colaborador',
                color='#add8e6'
            ),
        }

        return fig_charts

    def define_figs_by_months(self):
        fig_charts = {
            'fig_mes_html': generate_grouped_chart(
                self.agendados,
                status='Agendado',
                field_name='Areas__vegetacao__nome',
                title='Serviços por Mês/vegetação (Agendado)',
                label_type='vegetação'
            ),
        }

        return fig_charts


