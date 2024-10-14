from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from django.urls import reverse
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions, verify_login
from servicos.models_jardinagem import ServicoJardinagemAgendado
from empresasecundario.utils import define_empresas
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField
from django.shortcuts import redirect

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
        userid=userid,
        DataDeInicio='None',
        DataDeConclusao='None',
        TipoServico='None',
        Areas='None',
        ServicosEscalados=['None'],
        ColaboradoresEscalados=['None'],
        status=['Concluido']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'tipodeempresa', 'label': 'Tipo de empresa'},
        {'nome': 'empresaprestadora', 'label': 'Empresa'},
        {'nome': 'data_de_inicio', 'label': 'Data de inicio'},
        {'nome': 'area_atendida', 'label': 'Área atendida'},
        {'nome': 'id_agendamento', 'label': 'id agendamento'},
        {'nome': 'tipo_agendamento', 'label': 'Tipo de agendamento'},
        {'nome': 'descricao_do_servico', 'label': 'Descrição serviço'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaboradores'},
        {'nome': 'servicos_solicitados', 'label': 'Servicos solicitados'},
        {'nome': 'status_servico', 'label': 'Status'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Serviços concluidos, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_concluidos',
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_xlsx_concluidos', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços concluidos, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_concluidos',
                kwargs={'userid': userid}
            )
        })

    return generic_view(
        request=request,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem xlsx - Concluidos',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'area_atendid_id',
            'TipoServico': 'tipo_de_servico',
            'ServicosEscalados': 'servicos_solicitados_id',
            'ColaboradoresEscalados': 'colaboradores_chamados_id',
            'DataDeInicio': 'data_de_inicio',
            'DataDeConclusao': 'data_de_conclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        status=['Concluido'],
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
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

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'Areas', 'label': 'Área atendida'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'novo_status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Serviços agendados, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_agendados',
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_xlsx_agendados', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços agendados, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_agendados',
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
        app_name='relatório de serviços jardinagem xlsx - Planejados',
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
        button_export_tittle='Exportar Excel',
        status=['Agendado', 'Em andamento'],
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
        modal_button=False,
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view
    )
