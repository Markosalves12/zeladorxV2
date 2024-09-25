from django.shortcuts import reverse
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
        'status_agendamento': servico.status_agendamento,
        'status': servico.status,
        'dataconclusao': servico.DataDeConclusao,
    }