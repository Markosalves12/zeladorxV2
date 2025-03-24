from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from utils.utils import generate_id_random
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from relatorios.limpeza_predial.utils import graphs_limpeza_predial_concluido_to_reports
from areas.models_limpeza_predial import AreaLimpezaPredial
from datetime import datetime
from django.shortcuts import redirect
from permissionscontrol.utils import verify_login

def exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf(request, userid, id_random, DataDeInicio,
                                                              DataDeConclusao, Areas, TipoServico, ServicosEscalados,
                                                              ColaboradoresEscalados, type):
    block = verify_login(request=request, userid=userid)

    if block:
        return redirect('logout')

    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        ServicosEscalados=ServicosEscalados,
        TipoServico=TipoServico,
        Areas=Areas,
        ColaboradoresEscalados=ColaboradoresEscalados,
        status=['Concluido']
    )

    if type == 'configuracao':
        dados = dados.filter(id_random_configuracao=id_random)
    elif type == 'areas':
        object = AreaLimpezaPredial.objects.get(id_random=id_random)
    elif type == 'gerente':
        dados = dados.filter(colaborador_envolvido_id_random=id_random)

    # Create PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    x = 50

    # Draw header
    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
    y = height - 120  # Starting position after header
    page_number = 1
    p.setFont("Helvetica", 10)

    if len(dados) > 0:
        for dado in dados:
            p.setFont('Helvetica-Bold', 10)
            p.drawString(x, y, f"Descrição: {dado.descricao_do_servico}")
            y -= 20

            p.setFont("Helvetica", 10)
            p.drawString(x, y, f'Data de Início: {dado.data_de_inicio.strftime("%d/%m/%Y %H:%M")}')
            y -= 20
            p.drawString(x, y, f'Data de Conclusão: {dado.data_de_conclusao.strftime("%d/%m/%Y %H:%M")}')
            y -= 20
            p.drawString(x, y, f"Área Atendida: {dado.area_atendida}")
            y -= 20
            p.drawString(x, y, f"Tamanho da Área Atendida: {dado.area_total} M²")
            y -= 20
            p.drawString(x, y, f"Serviços Escalados: {dado.servicos_solicitados}")
            y -= 20
            p.drawString(x, y, f"Colaboradores Escalados: {dado.colaborador_envolvido}")
            y -= 20

            def add_images_to_canvas(p, dado, x, y, type, area_object=None):
                def calculate_new_dimensions(img_width, img_height):
                    new_width = img_width / 2.4
                    new_height = img_height / 2.4
                    return new_width, new_height

                # Lista de imagens a serem exibidas: área (se aplicável), solicitação e entrega
                images = []

                # Adiciona a imagem da área se type == 'areas'
                if type == 'areas' and area_object:
                    image_path = area_object.foto.url if area_object.foto else os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')
                    images.append(("Área", image_path))

                # Adiciona a imagem da solicitação (assumindo que pode existir)
                if hasattr(dado, 'foto_solicitacao') and dado.foto_solicitacao:
                    images.append(("Na solicitação", dado.foto_solicitacao.url))
                else:
                    images.append(("Na solicitação", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')))

                # Adiciona a imagem da entrega
                if dado.foto_conclusao:
                    images.append(("Na entrega", dado.foto_conclusao.url))
                else:
                    images.append(("Na entrega", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')))

                # Processa as imagens duas por página
                for i in range(0, len(images), 2):
                    if i > 0:  # Nova página após a primeira combinação
                        draw_footer(p, width)
                        p.showPage()
                        draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
                        y = height - 120

                    # Primeira imagem da página
                    title1, path1 = images[i]
                    p.setFont("Helvetica", 10)
                    p.drawString(x, y, title1)
                    y -= 12
                    height1 = draw_image(path1, x, y, p)
                    y -= height1 + 10

                    # Segunda imagem da página (se existir)
                    if i + 1 < len(images):
                        title2, path2 = images[i + 1]
                        p.setFont("Helvetica", 10)
                        p.drawString(x, y, title2)
                        y -= 12
                        height2 = draw_image(path2, x, y, p)
                        y -= height2 + 10

            # Passar o objeto da área se type == 'areas'
            area_object = object if type == 'areas' else None
            add_images_to_canvas(p, dado, x, y, type, area_object)

            # Draw footer and start new page
            draw_footer(p, width)
            p.showPage()
            page_number += 1
            p.setFont("Helvetica", 10)
            y = height - 70

    else:
        p.showPage()
        page_number += 1
        p.setFont("Helvetica", 10)
        y = height - 70

    if len(dados) > 0:
        (figs_concluidos_localidade,
         figs_concluidos_area,
         figs_concluidos_servico) = graphs_limpeza_predial_concluido_to_reports(request, userid, dados)

        start_y = height - 100
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, start_y, "Volume de serviços concluídos")
        start_y -= 20

        start_y, end_page = add_figures_to_pdf(
            p,
            {
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_servico
            },
            start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    draw_footer(p, width, is_last_page=True)
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos Concluido {generate_id_random()}.pdf"'

    return response