from django.shortcuts import render, reverse
from areas.models_jardinagem import AreasJardins
from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.utils import paginate

# Create your views here.
def historico_de_servicos_areas_jardinagem(request, userid, id_random):
    objeto = AreasJardins.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        Areas__id_random=id_random,
    )

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=1
    )

    return render(
        request=request,
        template_name="history/history.html",
        context={
            'app_name': f'Histórico de serviços {objeto.nome}',
            'objeto': objeto,
            'foto_objeto': objeto.foto.url if objeto.foto else None,
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                viewname='exportar_relatorio_de_serivos_Jardinagem_pdf',
                kwargs={
                    'userid': userid,
                }
            )
        }
    )

def historico_de_servicos_catologo_de_servicos_jardinagem(request, userid, id_random):
    objeto = CatalogodeServicoJardinagem.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        ServicosEscalados__id_random=id_random,
    )

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=1
    )

    return render(
        request=request,
        template_name="history/history.html",
        context={
            'app_name': f'Histórico de serviços {objeto.nome}',
            'objeto': objeto,
            'foto_objeto': None,
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                'exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
                kwargs={
                    'userid': userid,
                    # 'id_random': id_random
                }
            )
        }
    )