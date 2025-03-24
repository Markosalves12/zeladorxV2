from servicos.models_jardinagem import ServicoJardinagemAgendado
from areas.models_jardinagem import AreasJardins
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from utils.utils import formatar_atributos, generate_id_random
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from datetime import datetime
from relatorios.jardinagem.utils import graphs_jardinagem_concluido_to_reports
from django.shortcuts import redirect
from permissionscontrol.utils import verify_login

def exportar_relatorio_de_serivos_na_area_jardinagem_pdf(request, userid, id_random, DataDeInicio, DataDeConclusao, Areas,
                                                        TipoServico, ServicosEscalados, ColaboradoresEscalados, type):
    block = verify_login(request=request, userid=userid)

    if block:
        return redirect('logout')

    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    filters = dict()

    if DataDeInicio and DataDeInicio != "None":
        filters['DataDeInicio__gte'] = DataDeInicio
    if DataDeConclusao and DataDeConclusao != "None":
        filters['DataDeConclusao__lte'] = DataDeConclusao
    if Areas and Areas != "None":
        filters['Areas__id__in'] = Areas
    if TipoServico and TipoServico != "None":
        filters['TipoServico'] = TipoServico
    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['ServicosEscalados__id__in'] = ServicosEscalados
    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['ColaboradoresEscalados__id__in'] = ColaboradoresEscalados

    if type == 'catalogo_de_servicos':
        dados = ServicoJardinagemAgendado.objects.filter(**filters, status__in=['Concluido'])
    elif type == 'configuracao':
        dados = ServicoJardinagemAgendado.objects.filter(**filters, id_configuracao=id_random, status__in=['Concluido'])
    elif type == 'areas':
        object = AreasJardins.objects.get(id_random=id_random)
        dados = ServicoJardinagemAgendado.objects.filter(**filters, Areas__id_random=id_random, status__in=['Concluido'])
    elif type == 'gerente':
        dados = ServicoJardinagemAgendado.objects.filter(**filters, status__in=['Concluido'])

    # Create PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    x = 50

    # Draw header
    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 100  # Starting position after header
    page_number = 1
    p.setFont("Helvetica", 10)

    if len(dados) > 0:
        for dado in dados:
            p.setFont('Helvetica-Bold', 10)
            p.drawString(x, y, f"Descrição: {dado.DescricaoDoServico}")
            y -= 20

            p.setFont("Helvetica", 10)
            p.drawString(x, y, f'Data de Início: {dado.DataDeInicio.strftime("%d/%m/%Y %H:%M")}')
            y -= 20
            p.drawString(x, y, f'Data de Conclusão: {dado.DataDeConclusao.strftime("%d/%m/%Y %H:%M")}')
            y -= 20
            p.drawString(x, y, f"Área Atendida: {dado.Areas}")
            y -= 20
            p.drawString(x, y, f"Tamanho da Área Atendida: {dado.Areas.dimensao} M²")
            y -= 20

            # Serviços Escalados
            p.drawString(x, y, "Serviços Escalados:")
            y -= 10
            servicos = formatar_atributos(queryset=dado.ServicosEscalados.all(), atributo='nome')
            p.drawString(x + 20, y, f"- {servicos}")
            y -= 20

            # Colaboradores Escalados
            p.drawString(x, y, "Colaboradores Escalados:")
            y -= 10
            colaborador = formatar_atributos(queryset=dado.ColaboradoresEscalados.all(), atributo='username')
            p.drawString(x + 20, y, f"- {colaborador}")
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

                # Adiciona a imagem da solicitação
                if dado.foto_solicitacao:
                    images.append(("Na solicitação", dado.foto_solicitacao.url))
                else:
                    images.append(("Na solicitação", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')))

                # Adiciona a imagem da entrega
                if dado.foto_entrega:
                    images.append(("Na entrega", dado.foto_entrega.url))
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

    start_y = height - 100
    p.setFont('Helvetica-Bold', 12)

    if len(dados) > 0:
        (figs_concluidos_terreno, figs_concluidos_vegetacao, figs_concluidos_localidade,
         figs_concluidos_area, figs_concluidos_colaborador,
         figs_concluidos_servico) = graphs_jardinagem_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, "Volume de serviços prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p,
            {
                **figs_concluidos_terreno, **figs_concluidos_vegetacao, **figs_concluidos_localidade,
                **figs_concluidos_area, **figs_concluidos_colaborador, **figs_concluidos_servico
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
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {generate_id_random()}.pdf"'

    return response