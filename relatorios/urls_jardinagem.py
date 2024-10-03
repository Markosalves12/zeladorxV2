from django.urls import path

from relatorios.jardinagem.views_relatorios_jardinagem_xlsx import (relatorios_de_servicos_jardinagem_xlsx_agendados,
                                                                    relatorios_de_servicos_jardinagem_xlsx_concluidos)

from relatorios.jardinagem.views_relatorios_jardinagem_pdf import (relatorios_de_servicos_jardinagem_pdf_concluidos,
                                                                   relatorios_de_servicos_jardinagem_pdf_agendados)

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_xlsx import exportar_relatorio_de_serivos_Jardinagem_excel

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_pdf import exportar_relatorio_de_serivos_Jardinagem_pdf

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_pdf import (
    exportar_relatorio_de_serivos_na_area_jardinagem_pdf
)

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_xlsx import (
    exportar_relatorio_de_serivos_na_area_Jardinagem_excel
)


urlpatterns = [
    path(
        'relatorios_de_servicos_jardinagem_xlsx_concluidos/<str:userid>',
        relatorios_de_servicos_jardinagem_xlsx_concluidos,
        name='relatorios_de_servicos_jardinagem_xlsx_concluidos'
    ),
    path(
        'relatorios_de_servicos_jardinagem_xlsx_agendados/<str:userid>',
        relatorios_de_servicos_jardinagem_xlsx_agendados,
        name='relatorios_de_servicos_jardinagem_xlsx_agendados'
    ),
    path(
        'exportar_relatorio_de_serivos_Jardinagem_excel/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_excel,
        name='exportar_relatorio_de_serivos_Jardinagem_excel'
    ),
    path(
        'exportar_relatorio_de_serivos_Jardinagem_pdf/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_pdf,
        name='exportar_relatorio_de_serivos_Jardinagem_pdf'
    ),
    path(
        'relatorios_de_servicos_jardinagem_pdf_concluidos/<str:userid>',
        relatorios_de_servicos_jardinagem_pdf_concluidos,
        name='relatorios_de_servicos_jardinagem_pdf_concluidos'
    ),
    path(
        'relatorios_de_servicos_jardinagem_pdf_agendados/<str:userid>',
        relatorios_de_servicos_jardinagem_pdf_agendados,
        name='relatorios_de_servicos_jardinagem_pdf_agendados'
    ),
    path(
        'exportar_relatorio_de_serivos_na_area_jardinagem_pdf/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_jardinagem_pdf,
        name='exportar_relatorio_de_serivos_na_area_jardinagem_pdf'
    ),
    path(
        'exportar_relatorio_de_serivos_na_area_Jardinagem_excel/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_Jardinagem_excel,
        name='exportar_relatorio_de_serivos_na_area_Jardinagem_excel'
    ),
]
