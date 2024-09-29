from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from django.urls import reverse
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def relatorios_de_servicos_limpeza_predial_xlsx_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        status=['Concluido']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'tipodeempresa', 'label': 'Tipo de empresa'},
        {'nome': 'empresaprestadora', 'label': 'Empresa'},
        {'nome': 'data_de_inicio', 'label': 'Data de inicio'},
        {'nome': 'id_agendamento', 'label': 'id agendamento'},
        {'nome': 'tipo_agendamento', 'label': 'Tipo de agendamento'},
        {'nome': 'descricao_do_servico', 'label': 'Descrição serviço'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaboradores'},
        {'nome': 'servicos_solicitados', 'label': 'Servicos solicitados'},
        {'nome': 'status_servico', 'label': 'Status'},
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
                kwargs={
                    'userid': userid,
                }
            )
        }
    ]

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços limpeza predial xlsx - Concluidos',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_limpeza_predial_excel',
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



def relatorios_de_servicos_limpeza_predial_xlsx_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
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

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            status__in=['Agendado', 'Em andamento']
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços jardinagem pdf - Planejados',
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_limpeza_predial_excel',
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
