from django.shortcuts import render
from areas.models_jardinagem import AreasJardins
from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem
from utils.utils import paginate

# Create your views here.
def historico_de_servicos_areas_jardinagem(request, id_random):
    objeto = AreasJardins.objects.get(id_random=id_random)

    objetos = ServicoJardinagemAgendado.objects.all()

    dados_paginados = paginate(request=request, data_objects=objetos, per_page=1)

    return render(
        request=request,
        template_name="history/history.html",
        context={
            'app_name': f'Histórico de serviços {objeto.nome}',
            'objeto': objeto,
            'foto_objeto': objeto.foto.url if objeto.foto else None,
            'dados_paginados': dados_paginados
        }
    )

def exportar_pdf_historico_de_servicos_areas_jardinagem(request, id_random):
    pass