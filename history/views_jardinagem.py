from areas.models_jardinagem import AreasJardins
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.views import generic_view_history

# Create your views here.
def historico_de_servicos_areas_jardinagem(request, userid, id_random):
    objeto = AreasJardins.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        Areas__id_random=id_random,
        status__in=['Concluido']
    )

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto.nome}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='jardinagem_agendado',
        type_export='areas',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao',
            'Areas': 'Areas__id'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
        foto_objeto=None,
        Foto=False
    )

def historico_de_servicos_catologo_de_servicos_jardinagem(request, userid, id_random):
    objeto = CatalogodeServicoJardinagem.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        ServicosEscalados__id_random=id_random,
        status__in=['Concluido']
    )

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto.nome}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='jardinagem_agendado',
        type_export='catalogo_de_servicos',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
        foto_objeto=None,
        Foto=False
    )