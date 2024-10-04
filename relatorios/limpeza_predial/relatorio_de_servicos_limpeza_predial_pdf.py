from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from utils.utils import generate_id_random, define_range_time
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial, colect_dados_agendamentos_limpeza_predial
from relatorios.limpeza_predial.utils import (graphs_limpeza_predial__proximo_to_reports,
                                              graphs_limpeza_predial_atrasado_to_reports,
                                              graphs_limpeza_predial_agendado_to_reports,
                                              graphs_limpeza_predial_em_andamento_to_reports,
                                              graphs_limpeza_predial_concluido_to_reports)

from datetime import datetime

def exportar_relatorio_de_serivos_limpeza_predial_pdf(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                   TipoServico, ServicosEscalados, ColaboradoresEscalados):

    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

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

    if 'Concluido' in status.split(','):
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

    else:
        dados = colect_dados_agendamentos_limpeza_predial(
            request=request,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            TipoServico=TipoServico,
            ColaboradoresEscalados=ColaboradoresEscalados,
            Areas=Areas,
            status=status.split(',')
        )

    if len(dados) > 0:
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

    else:
        # Show the current page and prepare for the next record
        p.showPage()
        page_number += 1

        p.setFont("Helvetica", 10)  # Reset font size to 12 for new page content
        y = height - 70

    start_y = height - 100  # Posição inicial para o conteúdo após o cabeçalho
    p.setFont('Helvetica-Bold', 12)

    if 'Concluido' in status.split(',') and len(dados)>0:
        (figs_concluidos_localidade,
         figs_concluidos_area,
         figs_concluidos_servico) = graphs_limpeza_predial_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, {
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_servico
            }, start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    else:
        one_day, seven_days = define_range_time()

        graps_to_report = {}

        if len(dados.filter(data_de_inicio__gte=one_day, data_de_inicio__lte=seven_days)) > 0:
            (figs_proximo_localidade,figs_proximo_area,
             figs_proximo_servico,) = graphs_limpeza_predial__proximo_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_proximo_localidade,
                **figs_proximo_area,
                **figs_proximo_servico,
            )

        if len(dados.filter(data_de_inicio__lt=one_day)) > 0:
            (figs_atrasados__localidade, figs_atrasados__area,
             figs_atrasados__servico,) = graphs_limpeza_predial_atrasado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_atrasados__localidade,
                **figs_atrasados__area,
                **figs_atrasados__servico,
            )

        if len(dados.filter(data_de_inicio__gte=seven_days)) > 0:
            (figs_agendado_localidade,
             figs_agendado_area, figs_agendado_servico) = graphs_limpeza_predial_agendado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_agendado_localidade,
                **figs_agendado_area,
                **figs_agendado_servico,
            )

        if len(dados.filter(status_servico='Em andamento')) > 0:
            (figs_em_andamento_localidade,
             figs_em_andamento_area, figs_em_andamento_servico) = graphs_limpeza_predial_em_andamento_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_em_andamento_localidade,
                **figs_em_andamento_area,
                **figs_em_andamento_servico
            )

        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, graps_to_report, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height
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


