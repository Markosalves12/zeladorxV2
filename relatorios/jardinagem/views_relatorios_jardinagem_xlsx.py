from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from django.urls import reverse
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions

# Create your views here.
def relatorios_de_servicos_jardinagem_xlsx_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de jardinagem']
    )

    dados = colect_dados_fato_servico_jardinagem(
        request=request,
        status=['Concluido']
    )

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
        {'nome': 'Relatório de serviços', 'link': ''},
        {
            'nome': 'Serviços concluidos, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_concluidos',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Serviços concluidos, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_concluidos',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem xlsx - Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_Jardinagem_excel',
            kwargs={
                'userid': userid,
                'status': ','.join(['Concluido'])
            }
        ),
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )



def relatorios_de_servicos_jardinagem_xlsx_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de jardinagem']
    )

    dados = colect_dados_fato_servico_jardinagem(
        request=request,
        status=['Agendado', 'Em andamento']
    )

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
        {'nome': 'Relatório de serviços', 'link': ''},
        {
            'nome': 'Serviços agendados, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_agendados',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Serviços agendados, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_agendados',
                kwargs={'userid': userid}
            )
         }
    ]

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_agendado',
        app_name='relatório de serviços jardinagem pdf - Planejados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_Jardinagem_excel',
            kwargs={
                'userid': userid,
                'status': ','.join(['Agendado', 'Em andamento'])
            }
        ),
        modal_button=False,
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view
    )
