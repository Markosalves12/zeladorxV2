from servicos.models_jardinagem import ServicoJardinagemAgendado
from checklists.models import CheckListJardinagem
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO
import os
from django.conf import settings
from utils.utils import formatar_atributos
from relatorios.utils import draw_image, draw_footer, draw_header, add_figures_to_pdf
from utils.utils import generate_id_random, define_range_time
from datetime import datetime
from relatorios.jardinagem.utils import (graphs_jardinagem_proximo_to_reports,
                                         graphs_jardinagem_atrasado_to_reports,
                                         graphs_jardinagem_agendado_to_reports,
                                         graphs_jardinagem_em_andamento_to_reports,
                                         graphs_jardinagem_concluido_to_reports)
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect


def exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                        TipoServico, ServicosEscalados, ColaboradoresEscalados):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    DataDeInicio = datetime.strptime(DataDeInicio,
                                     '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao,
                                        '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    filters = dict()

    if DataDeInicio and DataDeInicio != "None":
        filters['DataDeInicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['DataDeConclusao__lte'] = DataDeConclusao

    if TipoServico and TipoServico != "None":
        filters['TipoServico'] = TipoServico

    if Areas and Areas != "None":
        filters['Areas__id'] = Areas

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['ServicosEscalados__id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['ColaboradoresEscalados__id__in'] = ColaboradoresEscalados

    dados = ServicoJardinagemAgendado.objects.filter(
        status__in=status.split(','),
        **filters
    )

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    x = 50

    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 120
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

            p.drawString(x, y, f'Data de conclusão: {dado.DataDeConclusao.strftime("%d/%m/%Y %H:%M")}')
            y -= 20

            p.drawString(x, y, f"Área atendida: {dado.Areas}")
            y -= 20

            p.drawString(x, y, f"Tamanho da área atendida: {dado.Areas.dimensao} M²")
            y -= 20

            p.drawString(x, y, "Serviços Escalados:")
            y -= 10
            servicos = formatar_atributos(queryset=dado.ServicosEscalados.all(), atributo='nome')
            p.drawString(x + 20, y, f"- {servicos}")
            y -= 20

            p.drawString(x, y, "Colaboradores Escalados:")
            y -= 10
            colaborador = formatar_atributos(queryset=dado.ColaboradoresEscalados.all(), atributo='username')
            p.drawString(x + 20, y, f"- {colaborador}")
            y -= 20

            def add_images_to_canvas(p, dado, x, y):
                def calculate_new_dimensions(img_width, img_height):
                    new_width = img_width / 2.4
                    new_height = img_height / 2.4
                    return new_width, new_height

                # Lista de imagens a serem exibidas: solicitação, checklists e entrega
                images = []

                # Adiciona a imagem da solicitação
                if dado.foto_solicitacao:
                    images.append(("Na solicitação", dado.foto_solicitacao.url, False))
                else:
                    images.append(
                        ("Na solicitação", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'), False))

                # Adiciona as imagens do checklist
                dados_checklist = CheckListJardinagem.objects.filter(servico_agendado__id_random=dado.id_random)
                for checklist in dados_checklist:
                    if checklist.foto_comprovacao:
                        images.append((checklist.descricao, checklist.foto_comprovacao.url, True, checklist.status))
                    else:
                        images.append((checklist.descricao,
                                       os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'), True,
                                       checklist.status))

                # Adiciona a imagem da entrega
                if dado.foto_entrega:
                    images.append(("Na entrega", dado.foto_entrega.url, False))
                else:
                    images.append(
                        ("Na entrega", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'), False))

                # Processa as imagens duas por página
                for i in range(0, len(images), 2):
                    if i > 0:  # Nova página após a primeira combinação
                        draw_footer(p, width)
                        p.showPage()
                        draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
                        y = height - 120

                    # Primeira imagem da página
                    title1, path1, is_checklist1 = images[i][0], images[i][1], images[i][2]
                    status1 = images[i][3] if is_checklist1 else None

                    if is_checklist1:
                        p.setFont("Helvetica", 8)  # Fonte menor para checklist
                        p.drawString(x + 40, y, f"Descrição: {title1}")  # Tabulação maior
                        y -= 12
                        p.setFont("Helvetica-Bold", 8)  # Fonte menor e negrito para status
                        status_text = f"Status: {status1}"
                        if status1 == "Pendente":
                            p.setFillColor(HexColor("#f6be04"))  # Amarelo
                            p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                        elif status1 == "Concluído":
                            p.setFillColor(HexColor("#008000"))  # Verde
                            p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                        p.setFillColor(HexColor("#000000"))
                        p.drawString(x + 40, y, status_text)
                        y -= 12
                        height1 = draw_image(path1, x + 40, y, p)  # Tabulação maior
                    else:
                        p.setFont("Helvetica", 10)
                        p.drawString(x, y, title1)
                        y -= 12
                        height1 = draw_image(path1, x, y, p)
                    y -= height1 + 10

                    # Segunda imagem da página (se existir)
                    if i + 1 < len(images):
                        title2, path2, is_checklist2 = images[i + 1][0], images[i + 1][1], images[i + 1][2]
                        status2 = images[i + 1][3] if is_checklist2 else None

                        if is_checklist2:
                            p.setFont("Helvetica", 8)  # Fonte menor para checklist
                            p.drawString(x + 40, y, f"Descrição: {title2}")  # Tabulação maior
                            y -= 12
                            p.setFont("Helvetica-Bold", 8)  # Fonte menor e negrito para status
                            status_text = f"Status: {status2}"
                            if status2 == "Pendente":
                                p.setFillColor(HexColor("#f6be04"))  # Amarelo
                                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                            elif status2 == "Concluído":
                                p.setFillColor(HexColor("#008000"))  # Verde
                                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                            p.setFillColor(HexColor("#000000"))
                            p.drawString(x + 40, y, status_text)
                            y -= 12
                            height2 = draw_image(path2, x + 40, y, p)  # Tabulação maior
                        else:
                            p.setFont("Helvetica", 10)
                            p.drawString(x, y, title2)
                            y -= 12
                            height2 = draw_image(path2, x, y, p)
                        y -= height2 + 10

            add_images_to_canvas(p, dado, x, y)

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

    if 'Concluido' in status.split(',') and len(dados) > 0:
        (figs_concluidos_terreno, figs_concluidos_vegetacao, figs_concluidos_localidade,
         figs_concluidos_area, figs_concluidos_colaborador,
         figs_concluidos_servico) = graphs_jardinagem_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, f"Volume de serviços prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p,
            {
                **figs_concluidos_terreno,
                **figs_concluidos_vegetacao,
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_colaborador,
                **figs_concluidos_servico
            },
            start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    else:
        one_day, seven_days = define_range_time()
        graps_to_report = {}

        if len(dados.filter(DataDeInicio__gte=one_day, DataDeInicio__lte=seven_days)) > 0:
            (figs_proximo_terreno, figs_proximo_vegetacao, figs_proximo_localidade, figs_proximo_area,
             figs_proximo_colaborador, figs_proximo_servico) = graphs_jardinagem_proximo_to_reports(request, userid,
                                                                                                    dados)
            graps_to_report.update(**figs_proximo_terreno, **figs_proximo_vegetacao, **figs_proximo_localidade,
                                   **figs_proximo_area, **figs_proximo_colaborador, **figs_proximo_servico)

        if len(dados.filter(DataDeInicio__lt=one_day)) > 0:
            (figs_atrasados_terreno, figs_atrasados__vegetacao, figs_atrasados__localidade, figs_atrasados__area,
             figs_atrasados__colaborador, figs_atrasados__servico) = graphs_jardinagem_atrasado_to_reports(request,
                                                                                                           userid,
                                                                                                           dados)
            graps_to_report.update(**figs_atrasados_terreno, **figs_atrasados__vegetacao, **figs_atrasados__localidade,
                                   **figs_atrasados__area, **figs_atrasados__colaborador, **figs_atrasados__servico)

        if len(dados.filter(DataDeInicio__gte=seven_days)) > 0:
            (figs_agendado_terreno, figs_agendado_vegetacao, figs_agendado_localidade,
             figs_agendado_area, figs_agendado_colaborador,
             figs_agendado_servico) = graphs_jardinagem_agendado_to_reports(request, userid, dados)
            graps_to_report.update(**figs_agendado_terreno, **figs_agendado_vegetacao, **figs_agendado_localidade,
                                   **figs_agendado_area, **figs_agendado_colaborador, **figs_agendado_servico)

        if len(dados.filter(status='Em andamento')) > 0:
            (figs_em_andamento_terreno, figs_em_andamento_vegetacao, figs_em_andamento_localidade,
             figs_em_andamento_area, figs_em_andamento_colaborador,
             figs_em_andamento_servico) = graphs_jardinagem_em_andamento_to_reports(request, userid, dados)
            graps_to_report.update(**figs_em_andamento_terreno, **figs_em_andamento_vegetacao,
                                   **figs_em_andamento_localidade,
                                   **figs_em_andamento_area, **figs_em_andamento_colaborador,
                                   **figs_em_andamento_servico)

        p.drawString(50, start_y, f"Volume de serviços Agendados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, graps_to_report, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height)

    draw_footer(p, width, is_last_page=True)
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.pdf"'
    return response