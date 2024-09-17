from django.urls import path
from relatorios.limpeza_predial.views_relatorios_limpeza_predial_xlsx import (relatorios_de_servicos_limpeza_predial_xlsx_agendados,
                                                                              relatorios_de_servicos_limpeza_predial_xlsx_concluidos)
from relatorios.limpeza_predial.views_relatorios_limpeza_predial_pdf import (relatorios_de_servicos_limpeza_predial_pdf_concluidos,
                                                                             relatorios_de_servicos_limpeza_predial_pdf_agendados)
from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_xlsx import exportar_relatorio_de_serivos_limpeza_predial_excel
from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_pdf import exportar_relatorio_de_serivos_limpeza_predial_pdf
from relatorios.limpeza_predial.relatorio_de_servicos_na_area_limpeza_predial_pdf import exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf


urlpatterns = [
    path('relatorios_de_servicos_limpeza_predial_xlsx_concluidos/<str:userid>', relatorios_de_servicos_limpeza_predial_xlsx_concluidos, name='relatorios_de_servicos_limpeza_predial_xlsx_concluidos'),
    path('relatorios_de_servicos_limpeza_predial_xlsx_agendados/<str:userid>', relatorios_de_servicos_limpeza_predial_xlsx_agendados, name='relatorios_de_servicos_limpeza_predial_xlsx_agendados'),
    path('exportar_relatorio_de_serivos_limpeza_predial_excel/<str:userid>', exportar_relatorio_de_serivos_limpeza_predial_excel, name='exportar_relatorio_de_serivos_limpeza_predial_excel'),
    path('exportar_relatorio_de_serivos_limpeza_predial_pdf/<str:userid>', exportar_relatorio_de_serivos_limpeza_predial_pdf, name='exportar_relatorio_de_serivos_limpeza_predial_pdf'),
    path('relatorios_de_servicos_limpeza_predial_pdf_concluidos/<str:userid>', relatorios_de_servicos_limpeza_predial_pdf_concluidos, name='relatorios_de_servicos_limpeza_predial_pdf_concluidos'),
    path('relatorios_de_servicos_limpeza_predial_pdf_agendados/<str:userid>', relatorios_de_servicos_limpeza_predial_pdf_agendados, name='relatorios_de_servicos_limpeza_predial_pdf_agendados'),
    path('exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf/<str:userid>/<str:id_random>', exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf, name='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf'),
]
