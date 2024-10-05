from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from utils.views import generic_view
from django.urls import reverse
from permissionscontrol.utils import validate_permissions
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField
from empresasecundario.utils import define_empresas
from django.shortcuts import redirect


def relatorios_de_servicos_limpeza_predial_pdf_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['311: Pode extrair relatórios PDF de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'Areas', 'label': 'Área atendida'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'status', 'label': 'Status'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1,         {
            'nome': 'Serviços concluidos, Jardinagem PDF',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_concluidos',
                kwargs={'userid': userid}
            )
        },)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços concluidos, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_concluidos',
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_jardinagem_pdf_concluidos', userid)

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado.objects.filter(
            status__in=['Concluido']
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços limpeza predial pdf - Concluidos',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link='exportar_relatorio_de_serivos_limpeza_predial_pdf',
        status=['Concluido'],
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )


def relatorios_de_servicos_limpeza_predial_pdf_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['311: Pode extrair relatórios PDF de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'Areas', 'label': 'Área atendida'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'novo_status', 'label': 'Status'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Serviços agendados, Jardinagem PDF',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_pdf_agendados',
                kwargs={'userid': userid}
            )
        },)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,         {
            'nome': 'Serviços agendados, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_agendados',
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_jardinagem_pdf_agendados', userid)


    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    return generic_view(
        request=request,
        model=ServicoLimpezaPredialAgendado.objects.filter(
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
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços Limpeza predial pdf - Planejados',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar PDF',
        button_export_link='exportar_relatorio_de_serivos_limpeza_predial_pdf',
        status=['Agendado', 'Em andamento'],
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )