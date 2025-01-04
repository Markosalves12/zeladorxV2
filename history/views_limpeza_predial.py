from areas.models_limpeza_predial import AreaLimpezaPredial
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from utils.views import generic_view_history
from permissionscontrol.utils import validate_permissions


# Create your views here.
def historico_de_servicos_areas_limpeza_predial(request, userid, id_random):
    permission_extract_pdf = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['311: Pode extrair relatórios PDF de limpeza predial']
    )

    permission_extract_xlsx = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    objeto = AreaLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio='None',
        DataDeConclusao='None',
        TipoServico='None',
        Areas='None',
        ServicosEscalados=['None'],
        ColaboradoresEscalados=['None'],
        status=['Concluido']
    ).filter(
        id_random_area=id_random
    ).distinct()

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto.nome}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='fato_limpeza_predial',
        type_export='areas',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'TipoServico': 'tipo_de_servico',
            'ServicosEscalados': 'servicos_solicitados_id',
            'DataDeInicio': 'data_de_inicio',
            'DataDeConclusao': 'data_de_conclusao',
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel',
        foto_objeto=objeto.fot.url,
        Foto=True,
        redirect_close_button='areas_limpeza_predial',
        permission_extract_pdf=permission_extract_pdf,
        permission_extract_xlsx=permission_extract_xlsx
    )


def historico_de_servicos_catologo_de_servicos_limpeza_predial(request, userid, id_random):
    permission_extract_pdf = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['311: Pode extrair relatórios PDF de limpeza predial']
    )

    permission_extract_xlsx = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    objeto = CatalogodeServicoLimpezaPredial.objects.get(
        id_random=id_random
    )

    objetos = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio='None',
        DataDeConclusao='None',
        TipoServico='None',
        Areas='None',
        ServicosEscalados=['None'],
        ColaboradoresEscalados=['None'],
        status=['Concluido']
    ).filter(
        id_random_servico=id_random
    ).distinct()

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto.nome}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='fato_limpeza_predial',
        type_export='catalogo_de_servicos',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'TipoServico': 'tipo_de_servico',
            'ServicosEscalados': 'servicos_solicitados_id',
            'DataDeInicio': 'data_de_inicio',
            'DataDeConclusao': 'data_de_conclusao',
            'Areas': 'area_atendid_id'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf',
        export_excel='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel',
        foto_objeto=None,
        Foto=False,
        redirect_close_button='catalogo_de_servicos_limpeza_predial',
        permission_extract_pdf=permission_extract_pdf,
        permission_extract_xlsx=permission_extract_xlsx
    )
