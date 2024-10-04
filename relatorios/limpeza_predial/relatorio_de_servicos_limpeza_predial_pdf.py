from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings
from utils.utils import generate_id_random
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from dashboards.data_visualization_limpeza_predial import data_visualization_limpeza_predial_graphs
from servicos.utils_limpeza_predial import (colect_dados_fato_servico_limpeza_predial,
                                            colect_dados_agendamentos_limpeza_predial)
from datetime import datetime

def exportar_relatorio_de_serivos_limpeza_predial_pdf(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                   TipoServico, ServicosEscalados, ColaboradoresEscalados):

    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        ServicosEscalados=ServicosEscalados,
        TipoServico=TipoServico,
        ColaboradoresEscalados=ColaboradoresEscalados,
        Areas=Areas,
        status=status.split(',')
    )

    # cria um buffer para inserir os dados no pdf
    buffer = BytesIO()

    # cria um objeto pdf usando o buffer anterior
    p = canvas.Canvas(
        buffer,
        pagesize=letter
    )
    width, height = letter

    # defini a posição inicial do cursor
    x = 50

    header_image_path = os.path.join(settings.MEDIA_ROOT, 'static/dist/img/logo alt.png')

    # função que cria o cabeçalho propriamente falado

    # Draw the header for the first page
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
    y = height - 120  # Adjust starting position for content after the header
    page_number = 1
    p.setFont("Helvetica", 10)

    for dado in dados:
        # Add the data_inicio
        p.setFont('Helvetica-Bold', 10)
        p.drawString(x, y, f"Descrição: {dado.descricao_do_servico}")
        y -= 20

        p.setFont("Helvetica", 10)
        p.drawString(x, y, f'Data de Início: {dado.data_de_inicio.strftime("%d/%m/%Y %H:%M")}',)

        y -= 20

        p.drawString(x, y, f'Data de conclusão: {dado.data_de_conclusao.strftime("%d/%m/%Y %H:%M")}')
        y -= 20

        p.drawString(x, y, f"área atendida: {dado.area_atendida}")
        y -= 20

        p.drawString(x, y, f"Tamanho da área atendida: {dado.area_total} M²")
        y -= 20

        p.drawString(x, y, f"Serviços Escalados: {dado.servicos_solicitados}")
        y -= 20

        if 'Concluido' in status.split(','):
            p.drawString(x, y, f"Colaboradores Escalados: {dado.colaborador_envolvido}")
            y -= 20

            def add_images_to_canvas(p, dado, x, y):
                def calculate_new_dimensions(img_width, img_height):
                    new_width = img_width / 2.4
                    new_height = img_height / 2.4
                    return new_width, new_height

                # Draw the second image (foto)
                if dado.foto_conclusao:
                    y -= 7
                    p.drawString(x, y, "Na entrega")
                    y -= 7
                    image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_conclusao)
                else:
                    y -= 7
                    p.drawString(x, y, "Na entrega")
                    y -= 7
                    image_path = os.path.join(settings.MEDIA_ROOT, 'static/dist/img/not found.png')

                draw_image(image_path, x, y, p)

            add_images_to_canvas(p, dado, x, y)

        # Draw the footer on the current page
        draw_footer(p, width)

        # Show the current page and prepare for the next record
        p.showPage()
        page_number += 1

        p.setFont("Helvetica", 10)  # Reset font size to 12 for new page content
        y = height - 70

    start_y = height - 100  # Posição inicial para o conteúdo após o cabeçalho
    p.setFont('Helvetica-Bold', 12)

    if 'Concluido' in status.split(','):
        figs_concluidos = data_visualization_limpeza_predial_reports(request, userid).define_figs_concluidos()
        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, figs_concluidos, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height
        )

    else:
        figs_agendados = data_visualization_limpeza_predial_reports(request, userid).define_figs_agendados()
        figs_em_andamento = data_visualization_limpeza_predial_reports(request, userid).define_figs_em_andamento()
        figs_em_proximo = data_visualization_limpeza_predial_reports(request, userid).define_figs_proximos()
        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, {**figs_agendados, **figs_em_proximo, **figs_em_andamento}, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height
        )

    draw_footer(
        p,
        width,
        is_last_page=True
    )

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.pdf"'

    return response


