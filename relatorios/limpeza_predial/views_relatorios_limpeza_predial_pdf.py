from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from utils.views import generic_view
from django.urls import reverse


def relatorios_de_servicos_limpeza_predial_pdf_concluidos(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
    ]

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
        {
            'nome': 'Jardinagem',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_concluidos',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Limpeza predial',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_concluidos',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços limpeza predial pdf - Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_limpeza_predial_pdf', kwargs={'userid': userid}),
        link_tipos=tipos,
        modal_button=False,
        userid=userid
    )


def relatorios_de_servicos_limpeza_predial_pdf_agendados(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
    ]

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
        {
            'nome': 'Jardinagem',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_agendados',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Limpeza predial',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_agendados',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços Limpeza predial pdf - Planejados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_limpeza_predial_pdf', kwargs={'userid': userid}),
        link_tipos=tipos,
        modal_button=False,
        userid=userid
    )