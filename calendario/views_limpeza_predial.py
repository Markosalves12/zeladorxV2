from django.shortcuts import render, reverse, redirect
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from django.db.models.functions import Now
from django.db.models import F, ExpressionWrapper, IntegerField
from calendario.utils import format_event
from permissionscontrol.utils import validate_permissions
from django.contrib import messages
from utils.utils import aplicar_filtros_dinamicos
from empresasecundario.utils import define_empresas


def calendario_limpeza_predial(request, userid):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['372: Pode visualizar serviços configurados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['370: Pode configurar novos serviços']
    )

    permission_accompany = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    permission_cancel = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['328: Pode cancelar serviços agendados']
    )

    filtro_mapeamento = {
        'Areas': 'Areas__id',
        'TipoServico': 'TipoServico',
        'ServicosEscalados': 'ServicosEscalados__id',
        'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    agendado = ServicoLimpezaPredialAgendado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
    ).annotate(
        data_atual=Now(),
        status_agendamento=ExpressionWrapper(
            F('DataDeInicio') - F('data_atual'),
            output_field=IntegerField()
        )/(3600*24*1000000)
    )

    if request.method == 'GET':
        get_data = request.GET.dict()
        agendado = aplicar_filtros_dinamicos(agendado, get_data, filtro_mapeamento)

    tipos = [
        {'nome': 'Calendário de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('calendario_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('calendario_limpeza_predial', kwargs={'userid': userid})})
    else:
        return redirect('calendario_jardinagem', userid)

    formatted_events = [
        format_event(
            servico,
        )
        for servico in agendado
    ]

    return render(
        request=request,
        template_name='agendamentos/calendario.html',
        context={
            'formatted_events': formatted_events,
            'app_name': 'Calendário Limpeza Predial',
            'link_tipos': tipos,
            'url_agendamento': 'agendar_servico_limpeza_predial',
            'url_acompanhamento': 'realizar_servico_limpeza_predial_agendado',
            'url_edicao': 'editar_servico_limpeza_predial_agendado',
            'url_cancelamento': 'cancelar_servico_limpeza_predial',
            'url_conclusao': 'concluir_servico_limpeza_predial',
            'form_search': ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate,
            'permission_accompany': permission_accompany,
            'permission_cancel': permission_cancel
        }
    )
