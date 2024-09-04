from servicos.utils import colect_dados
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from django.urls import reverse
from utils.views import generic_view

# Create your views here.
def relatorios_de_servicos_xlsx_concluidos(request):
    dados = colect_dados()
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'tipodeempresa', 'label': 'Tipo de empresa'},
        {'nome': 'empresaprestadora', 'label': 'Empresa'},
        {'nome': 'id_agendamento', 'label': 'id agendamento'},
        {'nome': 'tipo_agendamento', 'label': 'Tipo de agendamento'},
        {'nome': 'descricao_do_servico', 'label': 'Descrição serviço'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaboradores'},
        {'nome': 'servicos_solicitados', 'label': 'Servicos solicitados'},
    ]

    tipos = [
        {'nome': 'Status serviços', 'link': ''},
        {'nome': 'Concluidos', 'link': reverse('relatorios_de_servicos_xlsx_concluidos')},
        {'nome': 'Planejados', 'link': reverse('relatorios_de_servicos_xlsx_agendados')}
    ]

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_agendado',
        app_name='relatório de servicos xlsx -  Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse('exportar_relatorio_de_serivos_excel'),
        link_tipos=tipos,
        modal_button=False,
    )



def relatorios_de_servicos_xlsx_agendados(request):
    dados = colect_dados()
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'tipodeempresa', 'label': 'Tipo de empresa'},
        {'nome': 'empresaprestadora', 'label': 'Empresa'},
        {'nome': 'id_agendamento', 'label': 'id agendamento'},
        {'nome': 'tipo_agendamento', 'label': 'Tipo de agendamento'},
        {'nome': 'descricao_do_servico', 'label': 'Descrição serviço'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaboradores'},
        {'nome': 'servicos_solicitados', 'label': 'Servicos solicitados'},
    ]

    tipos = [
        {'nome': 'Status serviços', 'link': ''},
        {'nome': 'Concluidos', 'link': reverse('relatorios_de_servicos_xlsx_concluidos')},
        {'nome': 'Planejados', 'link': reverse('relatorios_de_servicos_xlsx_agendados')}
    ]

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_agendado',
        app_name='relatório de servicos xlsx - Agendados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse('exportar_relatorio_de_serivos_excel'),
        modal_button=False,
        link_tipos=tipos
    )
