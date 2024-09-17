from django.shortcuts import render, reverse
from areas.models_limpeza_predial import AreaLimpezaPredial
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, FatoServicoLimpezaPredial
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from utils.utils import paginate

# Create your views here.
def historico_de_servicos_areas_limpeza_predial(request, userid, id_random):
    objeto = AreaLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = ServicoLimpezaPredialAgendado.objects.all()

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
            'dados_paginados': dados_paginados
        }
    )

def historico_de_servicos_catologo_de_servicos_limpeza_predial(request, userid, id_random):
    objeto = CatalogodeServicoLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = ServicoLimpezaPredialAgendado.objects.filter(
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
                viewname='exportar_relatorio_de_serivos_na_area_pdf',
                kwargs={
                    'id_random': id_random,
                    'categoria_servico_zeladoria': 'limpeza_predial'
                }
            )
        }
    )