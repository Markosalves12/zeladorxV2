from django.shortcuts import render, reverse
from areas.models_limpeza_predial import AreaLimpezaPredial
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from utils.utils import paginate

# Create your views here.
def historico_de_servicos_areas_limpeza_predial(request, userid, id_random):
    objeto = AreaLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = colect_dados_fato_servico_limpeza_predial(
        request=request,
        status=['Concluido']
    ).filter(
        Servico__Areas__id_random=id_random
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
            'Foto': True,
            'type': 'fato_limpeza_predial',
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'areas'
                }
            ),
            'export_excel': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'areas',
                }
            ),
        }
    )

def historico_de_servicos_catologo_de_servicos_limpeza_predial(request, userid, id_random):
    objeto = CatalogodeServicoLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = colect_dados_fato_servico_limpeza_predial(
        request=request,
        status=['Concluido']
    ).filter(
        id_random_servico=id_random
    )

    for dado in objetos:
        print(dado.foto_conclusao)

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
            'Foto': False,
            'type': 'fato_limpeza_predial',
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'catalogo_de_servicos',
                }
            ),
            'export_excel': reverse(
                viewname='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    'type': 'catalogo_de_servicos',
                }
            ),
        }
    )