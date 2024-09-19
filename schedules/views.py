from django.shortcuts import render
from schedules.management.comands.run_scheduled_task_limpeza_predial import agendar_servicos_limpeza_predial_configurados

# Create your views here.
def force_updates(request):
    agendar_servicos_limpeza_predial_configurados(request)
    return render(
        request,
        template_name='DataTableAndForms/DataTableAndForms.html'
    )