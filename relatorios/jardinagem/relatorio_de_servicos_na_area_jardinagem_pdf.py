from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from areas.models_jardinagem import AreasJardins
from areas.models_limpeza_predial import AreaLimpezaPredial
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings
from utils.utils import formatar_atributos
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from dashboards.data_visualization_jardinagem import data_visualization_jardinagem_reports
from utils.utils import generate_id_random


def exportar_relatorio_de_serivos_na_area_jardinagem_pdf(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                   TipoServico, ServicosEscalados, ColaboradoresEscalados, type):
    if type == 'catalogo_de_servicos':
        dados = ServicoJardinagemAgendado.objects.filter(
            ServicosEscalados__id_random=id_random,
            status__in=['Concluido']
        )

    elif type == 'configuracao':
        dados = ServicoJardinagemAgendado.objects.filter(
            id_configuracao=id_random,
            status__in=['Concluido']
        )

    elif type == 'areas':
        object = AreasJardins.objects.get(
            id_random=id_random
        )

        dados = ServicoJardinagemAgendado.objects.filter(
            Areas__id_random=id_random,
            status__in=['Concluido']
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
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    # draw_footer
    # Draw the header for the first page

    y = height - 100  # Adjust starting position for content after the header
    page_number = 1
    p.setFont("Helvetica", 10)

    # calculate_new_dimensions
    # draw_image
    # Draw the first image

    if type == 'areas':
        if object.foto:
            y -= 7
            p.drawString(x, y, "Área")
            y -= 7
            image_path = os.path.join(settings.MEDIA_ROOT, object.foto.name)
        else:
            y -= 7
            p.drawString(x, y, "Área")
            y -= 7
            image_path = os.path.join(settings.MEDIA_ROOT, 'static/dist/img/not found.png')

        height1 = draw_image(image_path, x, y, p)

        # Update y position for the next image
        y -= height1 + 10  # 10 is the space between images
        y -= 20

    for dado in dados:
        # Add the data_inicio
        p.setFont('Helvetica-Bold', 10)
        p.drawString(x, y, f"Descrição: {dado.DescricaoDoServico}")
        y -= 20

        p.setFont("Helvetica", 10)
        p.drawString(x, y, f'Data de Início: {dado.DataDeInicio.strftime("%d/%m/%Y %H:%M")}',)

        y -= 20

        p.drawString(x, y, f'Data de conclusão: {dado.DataDeConclusao.strftime("%d/%m/%Y %H:%M")}')
        y -= 20

        p.drawString(x, y, f"área atendida: {dado.Areas}")
        y -= 20

        p.drawString(x, y, f"Tamanho da área atendida: {dado.Areas.dimensao} M²")
        y -= 20

        # Add the servicos_escalados
        p.drawString(x, y, "Serviços Escalados:")
        y -= 10

        servicos = formatar_atributos(
            queryset=dado.ServicosEscalados.all(),
            atributo='nome'
        )
        p.drawString(x + 20, y, f"- {servicos}")  # Ajuste conforme o campo do modelo Servicos
        y -= 20

        # Add the colaboradores_escalados
        p.drawString(x, y, "Colaboradores Escalados:")
        y -= 10

        colaborador = formatar_atributos(
            queryset=dado.ColaboradoresEscalados.all(),
            atributo='username'
        )
        p.drawString(x + 20, y, f"- {colaborador}")  # Ajuste conforme o campo do modelo Colaboradores
        y -= 20

        def add_images_to_canvas(p, dado, x, y):
            #calculate_new_dimensions
            #draw_image
            # Draw the first image (foto_inicio)
            if dado.foto_solicitacao:
                y -= 7
                p.drawString(x, y, "Na solicitação")
                y -= 7
                image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_solicitacao.name)
            else:
                y -= 7
                p.drawString(x, y, "Na solicitação")
                y -= 7
                image_path = os.path.join(settings.MEDIA_ROOT, 'static/dist/img/not found.png')

            height1 = draw_image(image_path, x, y, p)

            # Update y position for the next image
            y -= height1 + 10  # 10 is the space between images

            # Draw the second image (foto)
            if dado.foto_entrega:
                y -= 7
                p.drawString(x, y, "Na entrega")
                y -= 7
                image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_entrega.name)
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



    fig_terreno = data_visualization_jardinagem_reports(request, userid).define_figs_concluidos()

    start_y = height - 100  # Posição inicial para o conteúdo após o cabeçalho

    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, start_y, f"Volume de servicos concluidos")
    start_y -= 20

    start_y, end_page = add_figures_to_pdf(p, fig_terreno, start_y, start_y + 1, header_image_path=header_image_path,
                                           width=width, height=height)

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
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {generate_id_random()}.pdf"'

    return response