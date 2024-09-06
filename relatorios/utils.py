from reportlab.lib.utils import ImageReader

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