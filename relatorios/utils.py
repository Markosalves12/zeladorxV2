from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
import plotly.io as pio
from reportlab.lib.pagesizes import letter

def calculate_new_dimensions(img_width, img_height):
    new_width = img_width / 2
    new_height = img_height / 2
    return new_width, new_height


def draw_image(image_path, x, y, p):
    try:
        img_data = ImageReader(image_path)
        img_width, img_height = img_data.getSize()
        new_width, new_height = calculate_new_dimensions(img_width, img_height)
        p.drawImage(img_data, x, y - new_height, width=new_width, height=new_height, mask='auto')
        return new_height
    except Exception as e:
        p.drawString(x, y, f"Erro ao carregar a imagem: {str(e)}")
        return 0


def draw_footer(c, width, is_last_page=False):
    c.setFont("Helvetica", 9)
    if is_last_page:
        last_page_text = "zeladorX"
        c.drawString((width - c.stringWidth(last_page_text, fontSize=12)) / 2, 50, last_page_text)

def save_plotly_fig_as_image(fig, file_path):
    """Save Plotly figure as an image."""
    pio.write_image(fig, file_path)

def draw_header(c, header_image_path, width, height):
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
                 image_bottom + 50, f"Relatório de Serviços")

    c.drawString((width - c.stringWidth(f"",
                                        "Helvetica-Bold", fontSize=12)) / 2,
                 image_bottom + 0,
                 f"")

    c.drawString((width - c.stringWidth(f"",
                                        "Helvetica-Bold", fontSize=12)) / 2,
                 image_bottom - 20,
                 f"")

    c.setFont("Helvetica", 12)  # Set font back to normal for the rest of the content


def add_figures_to_pdf(c, fig_dict, start_y, start_page, width, height, header_image_path):
    width, height = letter
    y = start_y
    page_number = start_page

    # Define o caminho do diretório onde as imagens serão salvas usando BASE_DIR
    image_dir = os.path.join(settings.BASE_DIR, 'media', 'images')

    # Cria o diretório se ele não existir
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    for fig_name, fig_html in fig_dict.items():
        fig_file_path = os.path.join(image_dir, f'{fig_name}.png')
        save_plotly_fig_as_image(fig_html, fig_file_path)

        if os.path.exists(fig_file_path):
            fig_image = ImageReader(fig_file_path)
            fig_img_width, fig_img_height = fig_image.getSize()
            if y - fig_img_height / 3 < 50:
                draw_footer(c, page_number, is_last_page=False)
                c.showPage()
                page_number += 1
                # draw_header(c, header_image_path, width, height)
                y = height - 150

            n = 2
            c.drawImage(fig_image, (width - fig_img_width / n) / 2, y - fig_img_height / n,
                        width=fig_img_width / n, height=fig_img_height / n, mask='auto')
            y -= fig_img_height / n + 20

    return y, page_number
