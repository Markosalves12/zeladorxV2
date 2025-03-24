from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.views import generic_view
from django.urls import reverse
from permissionscontrol.utils import validate_permissions, verify_login
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField, F
from empresasecundario.utils import define_empresas
from django.shortcuts import redirect
from django.db.models.functions import ExtractDay

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
        })
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_pdf_concluidos', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços concluidos, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_concluidos',
                kwargs={'userid': userid}
            )
        })

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado.objects.filter(
            status__in=['Concluido']
        ).distinct(),
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
        status=['Concluido'],
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_pdf',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist',
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
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_pdf_agendados', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,  {
            'nome': 'Serviços agendados, Limpeza predial PDF',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_pdf_agendados',
                kwargs={'userid': userid}
            )
        })

    one_day = timezone.now().date() + timedelta(days=1)
    seven_days = timezone.now().date() + timedelta(days=7)

    return generic_view(
        request=request,
        model=ServicoJardinagemAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            status__in=['Agendado', 'Em andamento']
        ).distinct().annotate(
            dias_diferenca=ExtractDay(F('DataDeInicio') - timezone.now()),
            novo_status=Case(
                When(status='Em andamento', then=Value('Em andamento')),
                When(dias_diferenca__lt=0, then=Value('Atrasado')),
                When(dias_diferenca__gte=0, dias_diferenca__lte=7, then=Value('Próximo')),
                When(dias_diferenca__gt=7, then=Value('Agendado')),
                default=Value('Desconhecido'),
                output_field=CharField()
            )
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem pdf - Planejados',
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
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_pdf',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist',
        status=['Agendado', 'Em andamento'],
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )
