from servicos.utils import colect_dados
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.views import generic_view
from django.urls import reverse


def relatorios_de_servicos_pdf_concluidos(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
    ]

    tipos = [
        {'nome': 'Status serviços', 'link': ''},
        {'nome': 'Concluidos', 'link': reverse('relatorios_de_servicos_pdf_concluidos')},
        {'nome': 'Planejados', 'link': reverse('relatorios_de_servicos_pdf_agendados')}
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços pdf - Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_pdf'),
        link_tipos=tipos,
        modal_button=False,
    )


def relatorios_de_servicos_pdf_agendados(request):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
    ]

    tipos = [
        {'nome': 'Status serviços', 'link': ''},
        {'nome': 'Concluidos', 'link': reverse('relatorios_de_servicos_pdf_concluidos')},
        {'nome': 'Planejados', 'link': reverse('relatorios_de_servicos_pdf_agendados')}
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços pdf - Planejados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_pdf'),
        link_tipos=tipos,
        modal_button=False,
    )