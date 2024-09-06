from django.shortcuts import render, reverse
from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models.functions import Now, TruncDate, ExtractDay
from django.db.models import F, Q, ExpressionWrapper, IntegerField, DurationField

# Create your views here.
def calendario_jardinagem(request, userid):
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

    def format_event(servico):
        # Define a cor com base no status_agendamento
        if servico.status == "Em andamento":
            background_color = "#000080"
            border_color = "#000080"

        elif servico.status == "Cancelado":
            background_color = "#808080 "
            border_color = "#808080"

        elif servico.status == "Concluido":
            background_color = "#add8e6  "
            border_color = "#add8e6 "

        elif servico.status_agendamento >= 0 and servico.status_agendamento <= 5:
            background_color = "#ffff00"
            border_color = "#ffff00"

        elif servico.status_agendamento < 0:
            background_color = "#FF0000"
            border_color = "#FF0000"

        elif servico.status_agendamento > 5:
            background_color = "#008000"
            border_color = "#008000"

        return {
            "id_random": servico.id_random,
            "title": servico.DescricaoDoServico,
            "start": f"new Date({servico.DataDeInicio.year}, {servico.DataDeInicio.month - 1}, {servico.DataDeInicio.day}, "
                     f"{servico.DataDeInicio.hour}, {servico.DataDeInicio.minute})",
            "end": f"new Date({servico.DataDeConclusao.year}, {servico.DataDeConclusao.month - 1}, "
                   f"{servico.DataDeConclusao.day}, {servico.DataDeConclusao.hour}, {servico.DataDeConclusao.minute})",
            "allDay": "false",
            "backgroundColor": background_color,
            "borderColor": border_color,
            "url": "{% url 'agendar_servico_jardinagem' %}",
            "url_acompanhemento": "{% url 'realizar_servico_jardinagem_agendado' %}",
            'status_agendamento': servico.status_agendamento,
            'status': servico.status,
            'dataconclusao': servico.DataDeConclusao,
        }

    formatted_events = [format_event(servico) for servico in agendado]

    return render(
        request=request,
        template_name='agendamentos/calendario.html',
        context={
            'formatted_events': formatted_events,
            'app_name': 'Calendário Jardinagem',
            'link_tipos': tipos,
            # 'app_name': 'Calendário de serviços jardinagem',
            # 'link_tipos': tipos,
            "url_agendamento": "agendar_servico_jardinagem",
        }
    )
#
# def tabeladedados(request):
#     return render(request, 'dados e formularios/dados e formularios.html')