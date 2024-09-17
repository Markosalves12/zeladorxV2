from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.views import generic_view
from django.urls import reverse
from permissionscontrol.utils import validate_permissions

def relatorios_de_servicos_jardinagem_pdf_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['311: Pode extrair relatórios PDF de jardinagem']
    )

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
            'nome': 'Serviços concluidos, Jardinagem PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_concluidos',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Serviços concluidos, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_concluidos',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem pdf - Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_Jardinagem_pdf', kwargs={'userid': userid}),
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )


def relatorios_de_servicos_jardinagem_pdf_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['311: Pode extrair relatórios PDF de jardinagem']
    )

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
            'nome': 'Serviços agendados, Jardinagem PDF',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_agendados',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Serviços agendados, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_agendados',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardibagem pdf - Planejados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse('exportar_relatorio_de_serivos_Jardinagem_pdf', kwargs={'userid': userid}),
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )