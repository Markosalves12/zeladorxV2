from django.urls import path
from relatorios.views_relatorios_xlsx import relatorios_de_servicos_xlsx_concluidos, relatorios_de_servicos_xlsx_agendados
from relatorios.views_relatorios_pdf import relatorios_de_servicos_pdf_concluidos, relatorios_de_servicos_pdf_agendados
from relatorios.relatorio_de_servicos_xlsx import exportar_relatorio_de_serivos_excel
from relatorios.relatorio_de_servicos_pdf import exportar_relatorio_de_serivos_pdf


urlpatterns = [
    # rota na raiz do sistema
    path('relatorios_de_servicos_xlsx_concluidos', relatorios_de_servicos_xlsx_concluidos, name='relatorios_de_servicos_xlsx_concluidos'),
    path('relatorios_de_servicos_xlsx_agendados', relatorios_de_servicos_xlsx_agendados, name='relatorios_de_servicos_xlsx_agendados'),
    path('exportar_relatorio_de_serivos_excel', exportar_relatorio_de_serivos_excel, name='exportar_relatorio_de_serivos_excel'),
    path('exportar_relatorio_de_serivos_pdf', exportar_relatorio_de_serivos_pdf, name='exportar_relatorio_de_serivos_pdf'),
    path('relatorios_de_servicos_pdf_concluidos', relatorios_de_servicos_pdf_concluidos, name='relatorios_de_servicos_pdf_concluidos'),
    path('relatorios_de_servicos_pdf_agendados', relatorios_de_servicos_pdf_agendados, name='relatorios_de_servicos_pdf_agendados'),
]
