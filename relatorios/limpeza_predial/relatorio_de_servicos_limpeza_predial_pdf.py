from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings
from utils.utils import formatar_atributos
from relatorios.utils import draw_image, draw_footer


def exportar_relatorio_de_serivos_limpeza_predial_pdf(request, userid):
    dados = ServicoJardinagemAgendado.objects.filter(
        # status="Concluido"
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
    def draw_header(c):
        # se o endereço da imagem existir
        if os.path.exists(header_image_path):
            # abri a imagem enviada como parametro
            header_image = ImageReader(header_image_path)
            # captura as dimensões da imagem
            header_img_width, header_img_height = header_image.getSize()
            # centraliza a imagem no topo
            x_centered = (width - header_img_width / 3) / 2
            c.drawImage(header_image, x_centered, height - header_img_height / 3 - 20, width=header_img_width / 3, height=header_img_height / 3, mask='auto')
            image_bottom = height - header_img_height / 2 - 20 - header_img_height / 2 - 20
        else:
            image_bottom = height  # Adjust if image is not found

        # Adiciona o titulo do relatório abaixo da imagem

        # configura da fonte e tamanho do titulo
        # c.setFont("Helvetica-Bold", 16)
        c.setFont("Helvetica-Bold", 14)
        # escrever o titulo do relatório
        c.drawString((width - c.stringWidth(f"Relatório de Serviços",
                                            "Helvetica-Bold", fontSize=12)) / 2,
                     image_bottom + 20, f"Relatório de Serviços")

        c.drawString((width - c.stringWidth(f"",
                                            "Helvetica-Bold", fontSize=12)) / 2,
                     image_bottom + 0,
                     f"")

        c.drawString((width - c.stringWidth(f"",
                                            "Helvetica-Bold", fontSize=12)) / 2,
                     image_bottom - 20,
                     f"")

        c.setFont("Helvetica", 12)  # Set font back to normal for the rest of the content

    # Draw the header for the first page
    draw_header(p)
    y = height - 150  # Adjust starting position for content after the header
    page_number = 1
    p.setFont("Helvetica", 10)

    for dado in dados:
        # Add the data_inicio
        p.setFont('Helvetica-Bold', 10)
        p.drawString(x, y, f"Descrição: {dado.DescricaoDoServico}")
        y -= 20

        p.setFont("Helvetica", 10)
        p.drawString(x, y, f"Data de Início: {dado.DataDeInicio.strftime('%d/%m/%Y')}",)

        y -= 20

        p.drawString(x, y, f"Data de conclusão: {dado.DataDeConclusao.strftime('%d/%m/%Y')}")
        y -= 20

        p.drawString(x, y, f"área atendida: {dado.Areas}")
        y -= 20

        p.drawString(x, y, f"Tamanho da área atendida: {dado.Areas.dimensao} M²")
        y -= 20

        # Add the servicos_escalados
        p.drawString(x, y, "Serviços Escalados:")
        y -= 20

        servicos = formatar_atributos(
            queryset=dado.ServicosEscalados.all(),
            atributo='nome'
        )
        p.drawString(x + 20, y, f"- {servicos}")  # Ajuste conforme o campo do modelo Servicos
        y -= 20

        # Add the colaboradores_escalados
        p.drawString(x, y, "Colaboradores Escalados:")
        y -= 20

        colaborador = formatar_atributos(
            queryset=dado.ColaboradoresEscalados.all(),
            atributo='username'
        )
        p.drawString(x + 20, y, f"- {colaborador}")  # Ajuste conforme o campo do modelo Colaboradores
        y -= 20


        def add_images_to_canvas(p, dado, x, y):
            def calculate_new_dimensions(img_width, img_height):
                new_width = img_width / 2.4
                new_height = img_height / 2.4
                return new_width, new_height

            # Draw the first image (foto_inicio)
            if dado.foto_solicitacao:
                y -= 7
                p.drawString(x, y, "Na solicitção")
                y -= 7
                image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_solicitacao.name)
            else:
                y -= 7
                p.drawString(x, y, "Na solicitção")
                y -= 7
                image_path = os.path.join(settings.MEDIA_ROOT, 'static/assets/image not found (1).png')

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
                image_path = os.path.join(settings.MEDIA_ROOT, 'static/assets/image not found (1).png')

            draw_image(image_path, x, y, p)


        add_images_to_canvas(p, dado, x, y)


        # Draw the footer on the current page
        draw_footer(p, page_number, width)

        # Show the current page and prepare for the next record
        p.showPage()
        page_number += 1

        p.setFont("Helvetica", 10)  # Reset font size to 12 for new page content
        y = height - 70

    draw_footer(
        p,
        page_number,
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
    response['Content-Disposition'] = 'attachment; filename="relatorio de servicos.pdf"'

    return response


