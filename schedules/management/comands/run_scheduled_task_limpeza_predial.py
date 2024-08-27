import schedules
import time
from django.core.management.base import BaseCommand
from servicos.models_limpeza_predial import ServicoLimpezaPredialConfigurado


def agendar_servicos_limpeza_predial_configurados():
    objetos = ServicoLimpezaPredialConfigurado.objects.all()

    for objeto in objetos:
        print(objeto)