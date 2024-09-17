from django.shortcuts import render, reverse
from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models.functions import Now, TruncDate, ExtractDay
from django.db.models import F, Q, ExpressionWrapper, IntegerField, DurationField
from calendario.utils import format_event
from permissionscontrol.utils import validate_permissions

# Create your views here.
def calendario_jardinagem(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['322: Pode visualizar serviços agendados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    permission_accompany = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    permission_cancel = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['328: Pode cancelar serviços agendados']
    )

    agendado = ServicoJardinagemAgendado.objects.all().annotate(
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
            # userid=userid,
            # url_agendamento='agendar_servico_jardinagem',
            # url_acompanahemnto='realizar_servico_jardinagem_agendado'
        )
        for servico in agendado
    ]

    return render(
        request=request,
        template_name='agendamentos/calendario.html',
        context={
            'formatted_events': formatted_events,
            'app_name': 'Calendário Jardinagem',
            'link_tipos': tipos,
            'url_agendamento': 'agendar_servico_jardinagem',
            'url_acompanhamento': 'realizar_servico_jardinagem_agendado',
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate,
            'permission_accompany': permission_accompany,
            'permission_cancel': permission_cancel
        }
    )