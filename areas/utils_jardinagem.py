# from areas.models_jardinagem import AreasJardins
# from django.db.models import F, ExpressionWrapper, CharField, FloatField
# from empresasecundario.utils import define_empresas
from dashboards.data_visualization_jardinagem import data_visualization_jardinagem_graphs
from django.db.models import Sum


# def collect_dados_areas_jardinagem(request, userid):
#     empresas = define_empresas(request=request, userid=userid)
#     empresas_primarias_ids = empresas['empresas_primarias_ids']
#     empresas_secundarias_ids = empresas['empresas_secundarias_ids']
#
#     dados = AreasJardins.objects.all().annotate(
#         nome_area=ExpressionWrapper(
#             F('nome'),
#             output_field=CharField()
#         ),
#         area_total=ExpressionWrapper(
#             F('dimensao'),
#             output_field=CharField()
#         ),
#         terrenos=ExpressionWrapper(
#             F('Terreno__nome'),
#             output_field=CharField()
#         ),
#         Vegetacao=ExpressionWrapper(
#             F('vegetacao__nome'),
#             output_field=CharField()
#         ),
#         Periodicidade=ExpressionWrapper(
#             F('periodicidade'),
#             output_field=CharField()
#         ),
#         Foto=ExpressionWrapper(
#             F('foto'),
#             output_field=CharField()
#         ),
#         Localidade=ExpressionWrapper(
#             F('localidade__nome'),
#             output_field=CharField()
#         ),
#         latitude_media=ExpressionWrapper(
#             F('localidade__lat_med'),
#             output_field=FloatField()
#         ),
#         longitude_media=ExpressionWrapper(
#             F('localidade__long_med'),
#             output_field=FloatField()
#         ),
#         Unidade=ExpressionWrapper(
#             F('localidade__unidade__nome'),
#             output_field=CharField()
#         ),
#         Status=ExpressionWrapper(
#             F('status'),
#             output_field=CharField()
#         ),
#     ).distinct().filter(
#         localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
#         localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
#     )
#
#     return dados

def data_visualization_jardinagem_indicadores(request, userid, dados):
    # Obter as unidades distintas
    unidades = dados.values_list('localidade__unidade__nome', flat=True).distinct().count()

    # Calcular a área total mobilizada
    area_total_mobilizada = dados.filter(status='Mobilizado').aggregate(
        total_mobilizada=Sum('dimensao')
    )['total_mobilizada'] or 0

    # Calcular a área total desmobilizada
    area_total_desmobilizada = dados.filter(status='Desmobilizado').aggregate(
        total_desmobilizada=Sum('dimensao')
    )['total_desmobilizada'] or 0

    # Obter as localidades distintas
    localidades = dados.values_list('localidade__nome', flat=True).distinct().count()

    return (unidades, area_total_mobilizada, area_total_desmobilizada, localidades)


def graphs_jardinagem_to_html(request, userid, dados):
    fig_area_unidades_mobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_unidades_mobilizadas',
        filters={'status': 'Mobilizado'},
        field_name='localidade__unidade__nome',
        title='Área Total por unidade (Mobilizadas)',
        label_type='Unidade',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_unidades_desmobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_unidades_desmobilizadas',
        filters={'status': 'Desmobilizado'},
        field_name='localidade__unidade__nome',
        title='Área Total por unidade (Desmobilizado)',
        label_type='Unidade',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_localidades_mobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_localidades_mobilizadas',
        filters={'status': 'Mobilizado'},
        field_name='localidade__nome',
        title='Área Total por localidade (Mobilizadas)',
        label_type='Localidade',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_localidades_desmobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_localidades_desmobilizadas',
        filters={'status': 'Desmobilizado'},
        field_name='localidade__nome',
        title='Área Total por localidade (Desmobilzadas)',
        label_type='Localidade',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_terrenos_mobilizados = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_terrenos_mobilizados',
        filters={'status': 'Mobilizado'},
        field_name='Terreno__nome',
        title='Área Total por terreno (Mobilizadas)',
        label_type='Terreno',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_terrenos_desmobilizados = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_terrenos_desmobilizados',
        filters={'status': 'Desmobilizado'},
        field_name='Terreno__nome',
        title='Área Total por terreno (Desmobilzadas)',
        label_type='Terreno',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_vegetacao_mobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_vegetacao_mobilizadas',
        filters={'status': 'Mobilizado'},
        field_name='vegetacao__nome',
        title='Área Total por vegetação (Mobilizadas)',
        label_type='Vegetação',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_vegetacao_desmobilizadas = data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_vegetacao_desmobilizadas',
        filters={'status': 'Desmobilizado'},
        field_name='vegetacao__nome',
        title='Área Total por vegetação (Desmobilzadas)',
        label_type='Vegetação',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_periodicidade= data_visualization_jardinagem_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_periodicidade',
        filters={'status': 'Mobilizado'},
        field_name='periodicidade',
        title='Área Total por periodicidade',
        label_type='Periodicidade',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    return (fig_area_unidades_mobilizadas, fig_area_unidades_desmobilizadas,
            fig_area_localidades_mobilizadas, fig_area_localidades_desmobilizadas,
            fig_area_terrenos_mobilizados, fig_area_terrenos_desmobilizados,
            fig_area_vegetacao_mobilizadas , fig_area_vegetacao_desmobilizadas, fig_area_periodicidade)