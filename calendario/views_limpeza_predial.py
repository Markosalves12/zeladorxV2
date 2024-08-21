from django.shortcuts import render, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from django.db.models.functions import Now, TruncDate, ExtractDay
from django.db.models import F, Q, ExpressionWrapper, IntegerField, DurationField


def calendario_limpeza_predial(request):
    agendado = ServicoLimpezaPredialAgendado.objects.all().annotate(
        data_atual=Now(),
        status_agendamento=ExpressionWrapper(
            F('DataDeInicio') - F('data_atual'),
            output_field=IntegerField()
        )/(3600*24*1000000)
    )

    tipos = [
        {'nome': 'Calendário de serviços', 'link': ''},
        {'nome': 'Jardinagem', 'link': reverse('calendario_jardinagem')},
        {'nome': 'Limpeza predial', 'link': reverse('calendario_limpeza_predial')}
    ]

