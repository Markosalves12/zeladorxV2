from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from schedules.management.comands.run_scheduled_task_limpeza_predial import (
    agendar_servicos_limpeza_predial_configurados)

scheduler = BackgroundScheduler()

# Adiciona o job para rodar todos os dias às 00:10
scheduler.add_job(agendar_servicos_limpeza_predial_configurados, 'cron', hour=0, minute=10)

# Inicia o agendador
scheduler.start()

# Mantém o programa rodando para que o agendador continue funcionando
try:
    while True:
        pass  # Simplesmente mantemos o programa rodando
except (KeyboardInterrupt, SystemExit):
    # Encerra o agendador de forma limpa em caso de interrupção
    scheduler.shutdown()
    print("Scheduler finalizado.")