from django.http import JsonResponse
from servicos.models_jardinagem import ServicoAgendado
from colaborador.models import Colaborador


# Create your views here.
def aceitar_servico(request, id_random, id_random_colaborador):
    servico = ServicoAgendado.objects.get(id_random=id_random)
    colaborador = Colaborador.objects.get(id_random=id_random_colaborador)

    if colaborador not in servico.ColaboradoresConfirmados.all() and not colaborador in servico.ColaboradoresNegados.all():
        servico.ColaboradoresConfirmados.add(colaborador)

    elif colaborador in servico.ColaboradoresNegados.all():
        servico.ColaboradoresNegados.remove(colaborador)
        servico.ColaboradoresConfirmados.add(colaborador)

    return JsonResponse({'status': 'success'})



def rejeitar_servico(request, id_random, id_random_colaborador):
    servico = ServicoAgendado.objects.get(id_random=id_random)
    colaborador = Colaborador.objects.get(id_random=id_random_colaborador)

    if colaborador not in servico.ColaboradoresConfirmados.all() and not colaborador in servico.ColaboradoresNegados.all():
        servico.ColaboradoresNegados.add(colaborador)

    elif colaborador in servico.ColaboradoresConfirmados.all():
        servico.ColaboradoresConfirmados.remove(colaborador)
        servico.ColaboradoresNegados.add(colaborador)

    return JsonResponse({'status': 'success'})
