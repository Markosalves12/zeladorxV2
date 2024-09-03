from django.shortcuts import render
from areas.models_limpeza_predial import AreaLimpezaPredial
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, FatoServicoLimpezaPredial

# Create your views here.
def historico_de_servicos_areas_limpeza_predial(request, id_random):
    objeto = AreaLimpezaPredial.objects.get(id_random=id_random)

    history_objetos = ServicoLimpezaPredialAgendado.objects.all()

    return render
