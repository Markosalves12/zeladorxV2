from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.views import generic_view
from django.urls import reverse
from permissionscontrol.utils import validate_permissions
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField


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
        {'nome': 'Areas', 'label': 'Área atendida'},
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
                'relatorios_de_servicos_jardinagem_pdf_concluidos',
                kwargs={'userid': userid}
            )
        },
        {
            'nome': 'Serviços concluidos, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_concluidos',
                kwargs={'userid': userid}
            )
        }
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado.objects.filter(
            status__in=['Concluido']
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem pdf - Concluidos',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_Jardinagem_pdf',
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
        {'nome': 'Areas', 'label': 'Área atendida'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'novo_status', 'label': 'Status'},
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

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado.objects.filter(
            status__in=['Agendado', 'Em andamento']
        ).annotate(
            novo_status=Case(
                When(status='Em andamento', then=Value('Em andamento')),
                When(DataDeInicio__gte=one_day, DataDeInicio__lt=seven_days, then=Value('Próximo')),
                When(status='Agendado', DataDeInicio__gte=seven_days, then=Value('Agendado')),
                When(DataDeInicio__lt=timezone.now(), then=Value('Atrasado')),
                default=Value('Desconhecido'),
                output_field=CharField()
            )
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardibagem pdf - Planejados',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'

        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link=reverse(
            'exportar_relatorio_de_serivos_Jardinagem_pdf',
            kwargs={
                'userid': userid,
                'status': ','.join(['Agendado', 'Em andamento'])
            }
        ),
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )
