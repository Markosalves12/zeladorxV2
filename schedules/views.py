from django.shortcuts import render
from schedules.management.comands.run_scheduled_task_limpeza_predial import agendar_servicos_limpeza_predial_configurados
from schedules.management.comands.run_scheduled_task_jardinagem import agendar_servicos_jardinagem_configurados
import schedule
import time
import threading

def iniciar_schedule():
    # Adiciona os agendamentos
    schedule.every().day.at('00:10').do(agendar_servicos_limpeza_predial_configurados)
    schedule.every().day.at('00:10').do(agendar_servicos_jardinagem_configurados)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Controla a thread do agendamento (global para ser reutilizada)
schedule_thread = None

# View para forçar as atualizações e reiniciar o schedule
def force_updates(request):
    global schedule_thread

    # Primeiro, limpar os agendamentos anteriores
    schedule.clear()

    # Se houver uma thread de agendamento já rodando, devemos interrompê-la
    if schedule_thread and schedule_thread.is_alive():
        # Encerramos a thread anterior se estiver ativa
        # Nota: Python não oferece uma maneira direta de "matar" uma thread
        # Portanto, apenas limpamos os agendamentos e criamos uma nova.
        schedule_thread = None  # Desabilitar a thread anterior

    # Inicia uma nova thread para o agendamento
    schedule_thread = threading.Thread(target=iniciar_schedule)
    schedule_thread.daemon = True  # Permite que a thread seja finalizada quando o programa principal terminar
    schedule_thread.start()

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )