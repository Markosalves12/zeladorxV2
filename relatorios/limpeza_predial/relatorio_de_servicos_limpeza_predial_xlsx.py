import openpyxl
from servicos.headers_report_limpeza_predial import headers_report_services, headers_report_services_schedules
from servicos.utils_limpeza_predial import (colect_dados_fato_servico_limpeza_predial,
                                            colect_dados_agendamentos_limpeza_predial)
from django.http import HttpResponse
from utils.utils import generate_id_random


def exportar_relatorio_de_serivos_limpeza_predial_excel(request, userid, status):
    wb = openpyxl.Workbook()
    ws = wb.active

    if 'Concluido' in status.split(','):
        # cabeçalhos da tabela exportada
        headers = headers_report_services

        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header_title

        # Adicione os dados do relatório ao arquivo Excel
        dados = colect_dados_fato_servico_limpeza_predial(
            request=request,
            status=status.split(',')
        )

        for row_num, row in enumerate(dados, start=2):
            row_data = [
                row.tipodeempresa, row.empresaprestadora,

                row.id_agendamento, row.tipo_agendamento,

                row.descricao_do_servico, row.servicos_solicitados, row.data_de_inicio,

                row.data_de_conclusao, row.status_servico,

                row.area_atendida, row.area_total,

                row.localidade, row.unidade,

                row.id_servico, row.tempo_na_area, row.colaborador_envolvido,

                row.colaborador_envolvido_id_random, row.foto_conclusao,

                row.data_hora_chegada, row.data_hora_retorno, row.data_hora_retorno,

                row.id_random_area
            ]
            for col_num, value in enumerate(row_data, start=1):
                cell = ws.cell(
                    row=row_num,
                    column=col_num
                )
                cell.value = value

    else:
        # cabeçalhos da tabela exportada
        headers = headers_report_services_schedules

        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header_title

        # Adicione os dados do relatório ao arquivo Excel
        dados = colect_dados_agendamentos_limpeza_predial(
            request=request,
            status=status.split(',')
        )

        for row_num, row in enumerate(dados, start=2):
            row_data = [
                row.tipodeempresa, row.empresaprestadora,

                row.id_agendamento, row.tipo_agendamento,

                row.descricao_do_servico, row.servicos_solicitados, row.data_de_inicio,

                row.data_de_conclusao, row.status_servico,

                row.area_atendida, row.area_total,

                row.localidade, row.unidade, row.id_random_area
            ]
            for col_num, value in enumerate(row_data, start=1):
                cell = ws.cell(
                    row=row_num,
                    column=col_num
                )
                cell.value = value


    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # cria um anexo que ´instalado no lado cliente
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.xlsx"'

    # Salve o arquivo Excel
    wb.save(response)

    # retorna a resposta
    # linha obrigatória
    # ou o sistema quebra
    return response