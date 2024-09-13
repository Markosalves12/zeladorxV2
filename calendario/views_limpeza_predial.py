from django.shortcuts import render, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from django.db.models.functions import Now, TruncDate, ExtractDay
from django.db.models import F, Q, ExpressionWrapper, IntegerField, DurationField
from calendario.utils import format_event
from permissionscontrol.utils import validate_permissions


def calendario_limpeza_predial(request, userid):
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

    agendado = ServicoLimpezaPredialAgendado.objects.all().annotate(
        data_atual=Now(),
        status_agendamento=ExpressionWrapper(
            F('DataDeInicio') - F('data_atual'),
            output_field=IntegerField()
        )/(3600*24*1000000)
    )

    tipos = [
        {'nome': 'Calendário de serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('calendario_jardinagem', kwargs={'userid': userid})},
        {'nome': 'Limpeza predial', 'link': reverse('calendario_limpeza_predial', kwargs={'userid': userid})},
    ]

    formatted_events = [
        format_event(
            servico,
            userid=userid,
            url_agendamento='agendar_servico_limpeza_predial',
            url_acompanahemnto='realizar_servico_limpeza_predial_agendado'
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
            "url_agendamento": "agendar_servico_limpeza_predial",
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate,
            'permission_accompany': permission_accompany,
            'permission_cancel': permission_cancel
        }
    )
