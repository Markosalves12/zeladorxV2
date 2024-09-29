from django.shortcuts import render
from schedules.management.comands.run_scheduled_task_limpeza_predial import agendar_servicos_limpeza_predial_configurados
from schedules.management.comands.run_scheduled_task_jardinagem import agendar_servicos_jardinagem_configurados
import schedule
import time
import threading

# Create your views here.
def iniciar_schedule():
    schedule.every().day.at('00:10').do(agendar_servicos_limpeza_predial_configurados)
    schedule.every().day.at('00:10').do(agendar_servicos_jardinagem_configurados)

    while True:
        schedule.run_pending()
        time.sleep(1)


# View para forçar as atualizações e iniciar o schedule
def force_updates(request):
    # Inicia o schedule em um thread separado para não bloquear a renderização da view
    schedule_thread = threading.Thread(target=iniciar_schedule)
    schedule_thread.start()

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )