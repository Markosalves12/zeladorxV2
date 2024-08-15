# import os
# import django
#
# # Definir o caminho para o settings do seu projeto
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
#
# # Inicializar o Django
# django.setup()
#
# # Importar o modelo
# from servicos.models import ServicoAgendado
#
# # Recuperar todos os objetos da tabela
# agendado = ServicoAgendado.objects.all()
#
# # Função para formatar os dados no formato desejado
# # Função para formatar os dados no formato desejado
# def format_event(servico):
#     return {
#         "title": f"'{servico.DescricaoDoServico}'",  # Adiciona aspas ao valor da chave title
#         "start": f"new Date({servico.DataDeInicio.year}, {servico.DataDeInicio.month - 1}, {servico.DataDeInicio.day}, {servico.DataDeInicio.hour}, {servico.DataDeInicio.minute})",
#         "allDay": "false",
#         "url": "'{% url 'agendar_servico' %}'"  # Certifique-se de que a URL está correta no contexto do seu projeto
#     }
#
# # Listar e formatar todos os serviços agendados
# formatted_events = [format_event(servico) for servico in agendado]
#
# # Armazenar os eventos formatados em uma nova lista
# event_list = []
#
# for event in formatted_events:
#     event_dict = {
#         "title": event["title"],
#         "start": event["start"],
#         "allDay": event["allDay"],
#         "url": event["url"]
#     }
#     event_list.append(event_dict)
#
# # Imprimir a nova lista
# print(event_list)
#
#
#
