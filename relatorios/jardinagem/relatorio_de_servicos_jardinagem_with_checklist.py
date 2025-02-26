from servicos.models_jardinagem import ServicoJardinagemAgendado
from checklists.models import CheckListJardinagem
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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


def relatorio_de_servicos_jardinagem_with_checklist(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                   TipoServico, ServicosEscalados, ColaboradoresEscalados):
    block = verify_login(request=request, userid=userid)

    if block == True:
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

    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')

    # função que cria o cabeçalho propriamente falado

    # Draw the header for the first page
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 120  # Adjust starting position for content after the header
    page_number = 1
    p.setFont("Helvetica", 10)


    if len(dados)>0:
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
                def calculate_new_dimensions(img_width, img_height):
                    new_width = img_width / 2.4
                    new_height = img_height / 2.4
                    return new_width, new_height

                # Draw the first image (foto_inicio)
                if dado.foto_solicitacao:
                    y -= 7
                    p.drawString(x, y, "Na solicitção")
                    y -= 7
                    # image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_solicitacao.name)
                    image_path = dado.foto_solicitacao.url
                else:
                    y -= 7
                    p.drawString(x, y, "Na solicitção")
                    y -= 7
                    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')

                height1 = draw_image(image_path, x, y, p)

                # Update y position for the next image
                y -= height1 + 10  # 10 is the space between images


                # entre solicitacao e entrga vamos inserir dados referentes ao check list
                # em algum local da funcao precisaremos instaciar os dados do check list especifico
                dados_checklist = CheckListJardinagem.objects.filter(
                    servico_agendado__id_random=dados.id_random
                )

                if dados_checklist > 0:
                    for dados_checklis in dados_checklist:
                        # Draw the first image (foto_inicio)
                        if dados_checklis.foto_comprovacao:
                            y -= 7
                            p.drawString(x, y, dados_checklis.descricao)
                            y -= 7
                            # image_path = os.path.join(settings.MEDIA_ROOT, dado.foto_solicitacao.name)
                            image_path = dado.foto_comprovacao.url
                        else:
                            y -= 7
                            p.drawString(x, y, dados_checklis.descricao)
                            y -= 7
                            image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')

                        height1 = draw_image(image_path, x, y, p)

                        # Update y position for the next image
                        y -= height1 + 10  # 10 is the space between images


                # Draw the second image (foto)
                if dado.foto_entrega:
                    y -= 7
                    p.drawString(x, y, "Na entrega")
                    y -= 7
                    image_path = dado.foto_entrega.url
                else:
                    y -= 7
                    p.drawString(x, y, "Na entrega")
                    y -= 7
                    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')

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
        (figs_concluidos_terreno, figs_concluidos_vegetacao, figs_concluidos_localidade,
         figs_concluidos_area, figs_concluidos_colaborador, figs_concluidos_servico) = graphs_jardinagem_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, f"Volume de servicos prestados")
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
            (figs_proximo_terreno,figs_proximo_vegetacao,figs_proximo_localidade,figs_proximo_area,
             figs_proximo_colaborador,figs_proximo_servico,) = graphs_jardinagem_proximo_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_proximo_terreno,
                **figs_proximo_vegetacao,
                **figs_proximo_localidade,
                **figs_proximo_area,
                **figs_proximo_colaborador,
                **figs_proximo_servico,
            )

        if len(dados.filter(DataDeInicio__lt=one_day)) > 0:
            (figs_atrasados_terreno, figs_atrasados__vegetacao, figs_atrasados__localidade, figs_atrasados__area,
             figs_atrasados__colaborador,figs_atrasados__servico,) = graphs_jardinagem_atrasado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_atrasados_terreno,
                **figs_atrasados__vegetacao,
                **figs_atrasados__localidade,
                **figs_atrasados__area,
                **figs_atrasados__colaborador,
                **figs_atrasados__servico,
            )

        if len(dados.filter(DataDeInicio__gte=seven_days)) > 0:
            (figs_agendado_terreno, figs_agendado_vegetacao, figs_agendado_localidade,
             figs_agendado_area, figs_agendado_colaborador, figs_agendado_servico) = graphs_jardinagem_agendado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_agendado_terreno,
                **figs_agendado_vegetacao,
                **figs_agendado_localidade,
                **figs_agendado_area,
                **figs_agendado_colaborador,
                **figs_agendado_servico,
            )

        if len(dados.filter(status='Em andamento')) > 0:
            (figs_em_andamento_terreno, figs_em_andamento_vegetacao, figs_em_andamento_localidade,
             figs_em_andamento_area, figs_em_andamento_colaborador, figs_em_andamento_servico) = graphs_jardinagem_em_andamento_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_em_andamento_terreno,
                **figs_em_andamento_vegetacao,
                **figs_em_andamento_localidade,
                **figs_em_andamento_area,
                **figs_em_andamento_colaborador,
                **figs_em_andamento_servico
            )

        p.drawString(50, start_y, f"Volume de servicos Agendados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, graps_to_report, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height)


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


