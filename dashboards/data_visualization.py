from django.db.models import Sum, Count
import plotly.graph_objs as go
from django.db.models.functions import TruncMonth
import calendar
from django.db.models import F
import pandas as pd
import plotly.express as px

def get_total_area(queryset, area_field='Areas__dimensao'):
    aggregate_result = queryset.aggregate(total_area=Sum(area_field))
    return aggregate_result['total_area'] if aggregate_result['total_area'] else 0


def calculate_areas_and_counts(dados_servicos, status, date_filter=None):
    """
    Calcula a soma das áreas e as contagens de itens para um conjunto de dados filtrados.
    """
    queryset = dados_servicos.filter(status=status)
    if date_filter:
        queryset = queryset.filter(date_filter)
    return get_total_area(queryset)

def get_total_area_by_category(queryset, category_field, sum_by, count_by):
    """
    Calcula a soma das áreas e as contagens de itens para cada categoria.

    Args:
        queryset: A consulta do Django ORM.
        category_field: O campo da categoria a ser agrupado.

    Returns:
        Um dicionário com a categoria como chave e a soma das áreas como valor.
        Um dicionário com a categoria como chave e a contagem de itens como valor.
    """
    data = queryset.values(category_field).annotate(
        total_area=Sum(sum_by),
        count=Count(count_by)
    ).order_by()

    total_area_by_category = {item[category_field]: item['total_area'] for item in data}
    counts_by_category = {item[category_field]: item['count'] for item in data}

    return total_area_by_category, counts_by_category


def plot_horizontal_bar_chart(data, title, x_axis_title, y_axis_title, counts, marker_color='#000080'):
    """
    Gera um gráfico de barras horizontais.

    Args:
        data: Um dicionário com a categoria como chave e a soma das áreas como valor.
        title: O título do gráfico.
        x_axis_title: O título do eixo x.
        y_axis_title: O título do eixo y.

    Returns:
        Uma figura Plotly do gráfico de barras horizontais.
    """
    categories = list(data.keys())
    values = list(data.values())
    hovertexts = [f'Área Total: {v}<br>Servicos: {counts[c]}' for c, v in data.items()]


    # Calcula a altura dinamicamente com base no número de categorias
    base_height = 300  # Altura base mínima
    extra_height_per_category = 20  # Altura adicional por categoria
    height = base_height + extra_height_per_category * len(categories)

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker_color=marker_color,
        width=0.3,
        text=hovertexts,
        textposition='auto',
        hovertext=hovertexts,
        hoverinfo='text'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        margin=dict(l=0, r=0, t=27, b=0),  # Ajustando as margens
        bargap=0.1,
        height=height
    )

    return fig


def get_total_area_and_counts_by_month(queryset, field_name, sum_by, count_by, date_column):
    """
    Calcula a soma das áreas e as contagens de itens para cada mês e campo especificado.

    Args:
        queryset: A consulta do Django ORM.
        field_name: O nome do campo para agrupamento (e.g., 'area__vegetacao', 'area__terreno').

    Returns:
        Um dicionário com o mês como chave e a soma das áreas como valor.
        Um dicionário com o mês como chave e a contagem de itens como valor.
        Um dicionário com o mês como chave e a categoria como valor.
    """
    data = queryset.annotate(
        month=TruncMonth(date_column),
        category=F(field_name)
    ).values('month', 'category').annotate(
        total_area=Sum(sum_by),
        count=Count(count_by)
    ).order_by('month', 'category')

    total_area_by_month = {}
    counts_by_month = {}
    categories_by_month = {}

    for item in data:
        month = item['month']
        category = item['category']
        month_str = f"{calendar.month_abbr[month.month]}/{month.year}"

        if month_str not in total_area_by_month:
            total_area_by_month[month_str] = {}
            counts_by_month[month_str] = {}
            categories_by_month[month_str] = {}

        total_area_by_month[month_str][category] = item['total_area']
        counts_by_month[month_str][category] = item['count']
        categories_by_month[month_str][category] = category

    return total_area_by_month, counts_by_month, categories_by_month


def plot_grouped_bar_chart(data, title, x_axis_title, y_axis_title, counts, categories, label_type, marker_colors=None):
    """
    Gera um gráfico de barras agrupadas.

    Args:
        data: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
              e a soma das áreas como valores internos.
        title: O título do gráfico.
        x_axis_title: O título do eixo x.
        y_axis_title: O título do eixo y.
        counts: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
                e a contagem de itens como valores internos.
        categories: Um dicionário aninhado com meses como chaves externas e categorias como chaves internas,
                    e o nome da categoria como valores internos.
        label_type: Uma string que especifica se é 'vegetação' ou 'terreno'.
        marker_colors: Lista de cores das barras.

    Returns:
        Uma string HTML contendo a figura Plotly do gráfico de barras agrupadas.
    """
    fig = go.Figure()

    months = list(data.keys())
    categories_list = list({cat for month in data.values() for cat in month.keys()})

    for i, category in enumerate(categories_list):
        values = [data[month].get(category, 0) for month in months]
        hovertexts = [
            f'{label_type.capitalize()}: {categories[month].get(category, "N/A")}<br>Mês: {month}<br>Área Total: {data[month].get(category, 0)}<br>Serviços: {counts[month].get(category, 0)}'
            for month in months
        ]

        fig.add_trace(go.Bar(
            x=months,
            y=values,
            name=category,
            width=0.3,
            marker_color=marker_colors[i] if marker_colors else None,
            text=hovertexts,
            textposition='auto',
            hovertext=hovertexts,
            hoverinfo='text',
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        barmode='group',
        margin=dict(l=0, r=0, t=27, b=0),  # Ajustando as margens
        height=300,
    )

    return fig


def generate_grouped_chart(dados_servicos, filters, field_name, title, label_type, sum_by, count_by, date_column):
    """
    Gera um gráfico de barras agrupadas para um conjunto de dados filtrados.
    """
    area, counts, categories = get_total_area_and_counts_by_month(
        dados_servicos.filter(**filters),
        field_name,
        sum_by,
        count_by,
        date_column
    )

    return plot_grouped_bar_chart(area, title, 'Mês', 'Área Total', counts, categories, label_type)



def generate_chart(dados_servicos, filters, field_name, title, label_type, color, sum_by, count_by):
    """
    Gera um gráfico de barras horizontais para um conjunto de dados filtrados.
    """
    area, counts = get_total_area_by_category(dados_servicos.filter(**filters), field_name, sum_by, count_by)
    return plot_horizontal_bar_chart(area, title, 'Área Total', label_type, counts, color)


def plot_map(paginated_queryset, color="#FF0000", scale_factor=2):
    """
    Gera um mapa interativo com bolhas proporcionais à área total de cada localidade usando px.scatter_mapbox.

    Args:
        paginated_queryset: Um queryset paginado contendo 'lat_localidade', 'long_localidade', 'area_total', 'unidade_nome' e 'localidade_nome'.
        color: Cor das bolhas no mapa (padrão: vermelho).
        scale_factor: Fator de escala para ajustar o tamanho das bolhas (padrão: 2).

    Returns:
        Uma figura Plotly do mapa interativo.
    """
    all_data = []

    # Coleta os dados do queryset paginado
    for page in paginated_queryset.paginator.page_range:
        current_page = paginated_queryset.paginator.page(page)
        for obj in current_page.object_list:
            all_data.append({
                'lat_localidade': float(obj['lat_localidade']),
                'long_localidade': float(obj['long_localidade']),
                'unidade_nome': obj['unidade_nome'],
                'area_total': float(obj['area_total']),
                'localidade_nome': obj['localidade_nome'],
            })

    # Criando o DataFrame
    df = pd.DataFrame(all_data)

    # Definição da centralização padrão do mapa (Brasília)
    map_center = {"lat": -15.797483, "lon": -47.935315}

    # Se não houver dados, retorna o mapa base com um marcador de "Nenhum dado disponível"
    if df.empty or len(df) == 0:
        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
            lat=[map_center["lat"]],
            lon=[map_center["lon"]],
            mode="markers+text",
            marker=dict(size=10, color="gray"),
            text=["Nenhum dado disponível"],
            textposition="top center",
        ))

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center=map_center,
            mapbox_zoom=5,
            margin=dict(l=0, r=0, t=50, b=0),
            height=700,
            title="<b>Nenhum dado disponível</b>"
        )

        return fig

    # Agrupando os dados por localidade
    grouped_df = df.groupby(["lat_localidade", "long_localidade", "unidade_nome", "localidade_nome"]).agg(
        area_total=("area_total", "sum"),
        area_media=("area_total", "mean"),
        num_areas=("area_total", "count")
    ).reset_index()

    # Criando o texto do tooltip
    grouped_df["hover_text"] = grouped_df.apply(
        lambda row: (
            f"{row['localidade_nome']}<br>"
            f"Unidade: {row['unidade_nome']}"
            f"<br>Total de Áreas: {row['num_areas']}"
            f"<br>Área Média: {row['area_media']:.2f} m²"
            f"<br>Área Total: {row['area_total']:.2f} m²"
        ), axis=1
    )

    # Definindo o tamanho das bolhas proporcional à área total, limitando o tamanho máximo em 25
    grouped_df["bubble_size"] = (grouped_df["area_total"] / grouped_df["area_total"].max()) * 30 * scale_factor
    grouped_df["bubble_size"] = grouped_df["bubble_size"].clip(lower=5, upper=25)

    # Criando o mapa com scatter_mapbox
    fig = px.scatter_mapbox(
        grouped_df,
        lat="lat_localidade",
        lon="long_localidade",
        size="bubble_size",
        hover_name="unidade_nome",
        hover_data={"area_total": True, "area_media": True, "num_areas": True},
        color_discrete_sequence=[color],
        text="hover_text",
        opacity=0.7,
        zoom=5,
    )

    fig.update_traces(marker=dict(sizemin=5))  # Define um tamanho mínimo para os pontos

    # Ajustando layout final
    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=50, b=0),
        height=700,
        font=dict(size=18),
        mapbox_center=map_center,
    )

    return fig