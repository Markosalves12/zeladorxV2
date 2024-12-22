import openpyxl
from servicos.headers_report_limpeza_predial import headers_report_services, headers_report_services_schedules
from servicos.utils_limpeza_predial import (colect_dados_fato_servico_limpeza_predial,
                                            colect_dados_agendamentos_limpeza_predial)
from django.http import HttpResponse
from utils.utils import generate_id_random
from datetime import datetime
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect

def exportar_relatorio_de_serivos_limpeza_predial_excel(
    request, userid, status, DataDeInicio, DataDeConclusao, Areas,
    TipoServico, ServicosEscalados, ColaboradoresEscalados
):
    # Verifica login
    block = verify_login(request=request, userid=userid)
    if block:
        return redirect('logout')

    # Cria o workbook e a planilha ativa
    wb = openpyxl.Workbook()
    ws = wb.active

    # Converte os parâmetros de entrada
    DataDeInicio = (
        datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M').replace(tzinfo=None)
        if DataDeInicio and DataDeInicio != "None" else None
    )
    DataDeConclusao = (
        datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M').replace(tzinfo=None)
        if DataDeConclusao and DataDeConclusao != "None" else None
    )
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')
    status_list = status.split(',')

    # Seleciona cabeçalhos e coleta dados
    if 'Concluido' in status_list:
        headers = headers_report_services
        dados = colect_dados_fato_servico_limpeza_predial(
            request=request,
            userid=userid,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            Areas=Areas,
            TipoServico=TipoServico,
            ColaboradoresEscalados=ColaboradoresEscalados,
            status=status_list
        )
    else:
        headers = headers_report_services_schedules
        dados = colect_dados_agendamentos_limpeza_predial(
            request=request,
            userid=userid,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            Areas=Areas,
            TipoServico=TipoServico,
            ColaboradoresEscalados=ColaboradoresEscalados,
            status=status_list
        )

    # Adiciona os cabeçalhos ao Excel
    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header_title

    # Adiciona os dados ao Excel
    for row_num, row in enumerate(dados, start=2):
        row_data = [
            row.tipodeempresa, row.empresaprestadora, row.id_agendamento,
            row.tipo_agendamento, row.descricao_do_servico, row.servicos_solicitados,
            row.data_de_inicio.replace(tzinfo=None) if row.data_de_inicio else None,
            row.data_de_conclusao.replace(tzinfo=None) if row.data_de_conclusao else None,
            row.status_servico, row.area_atendida, row.area_total, row.localidade,
            row.unidade, row.id_random_area, row.tempo_na_area if 'Concluido' in status_list else None,
            row.colaborador_envolvido if 'Concluido' in status_list else None,
            row.colaborador_envolvido_id_random if 'Concluido' in status_list else None,
            row.foto_conclusao if 'Concluido' in status_list else None,
            row.data_hora_chegada.replace(tzinfo=None) if row.data_hora_chegada else None,
            row.data_hora_retorno.replace(tzinfo=None) if row.data_hora_retorno else None
        ]
        row_data = [value for value in row_data if value is not None]  # Remove valores não aplicáveis
        for col_num, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="relatorio_de_servicos_{status}_{generate_id_random()}.xlsx"'

    # Salva o arquivo Excel na resposta
    wb.save(response)

    return response


# def exportar_relatorio_de_serivos_limpeza_predial_excel(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
#                                                    TipoServico, ServicosEscalados, ColaboradoresEscalados):
#     block = verify_login(request=request, userid=userid)
#
#     if block == True:
#         return redirect('logout')
#
#     wb = openpyxl.Workbook()
#     ws = wb.active
#
#     DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
#     DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
#     ServicosEscalados = ServicosEscalados.split(',')
#     ColaboradoresEscalados = ColaboradoresEscalados.split(',')
#
#     if 'Concluido' in status.split(','):
#         # cabeçalhos da tabela exportada
#         headers = headers_report_services
#
#         for col_num, header_title in enumerate(headers, 1):
#             cell = ws.cell(row=1, column=col_num)
#             cell.value = header_title
#
#         # Adicione os dados do relatório ao arquivo Excel
#         dados = colect_dados_fato_servico_limpeza_predial(
#             request=request,
#             userid=userid,
#             DataDeInicio=DataDeInicio,
#             DataDeConclusao=DataDeConclusao,
#             ServicosEscalados=ServicosEscalados,
#             Areas=Areas,
#             TipoServico=TipoServico,
#             ColaboradoresEscalados=ColaboradoresEscalados,
#             status=status.split(',')
#         )
#
#         for row_num, row in enumerate(dados, start=2):
#             row_data = [
#                 row.tipodeempresa, row.empresaprestadora,
#
#                 row.id_agendamento, row.tipo_agendamento,
#
#                 row.descricao_do_servico, row.servicos_solicitados, row.data_de_inicio,
#
#                 row.data_de_conclusao, row.status_servico,
#
#                 row.area_atendida, row.area_total,
#
#                 row.localidade, row.unidade,
#
#                 row.id_servico, row.tempo_na_area, row.colaborador_envolvido,
#
#                 row.colaborador_envolvido_id_random, row.foto_conclusao,
#
#                 row.data_hora_chegada, row.data_hora_retorno, row.data_hora_retorno,
#
#                 row.id_random_area
#             ]
#             for col_num, value in enumerate(row_data, start=1):
#                 cell = ws.cell(
#                     row=row_num,
#                     column=col_num
#                 )
#                 cell.value = value
#
#     else:
#         # cabeçalhos da tabela exportada
#         headers = headers_report_services_schedules
#
#         for col_num, header_title in enumerate(headers, 1):
#             cell = ws.cell(row=1, column=col_num)
#             cell.value = header_title
#
#         # Adicione os dados do relatório ao arquivo Excel
#         dados = colect_dados_agendamentos_limpeza_predial(
#             request=request,
#             userid=userid,
#             DataDeInicio=DataDeInicio,
#             DataDeConclusao=DataDeConclusao,
#             ServicosEscalados=ServicosEscalados,
#             Areas=Areas,
#             TipoServico=TipoServico,
#             ColaboradoresEscalados=ColaboradoresEscalados,
#             status=status.split(',')
#         )
#
#         for row_num, row in enumerate(dados, start=2):
#             row_data = [
#                 row.tipodeempresa, row.empresaprestadora,
#
#                 row.id_agendamento, row.tipo_agendamento,
#
#                 row.descricao_do_servico, row.servicos_solicitados, row.data_de_inicio,
#
#                 row.data_de_conclusao, row.status_servico,
#
#                 row.area_atendida, row.area_total,
#
#                 row.localidade, row.unidade, row.id_random_area
#             ]
#             for col_num, value in enumerate(row_data, start=1):
#                 cell = ws.cell(
#                     row=row_num,
#                     column=col_num
#                 )
#                 cell.value = value
#
#
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     # cria um anexo que ´instalado no lado cliente
#     response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.xlsx"'
#
#     # Salve o arquivo Excel
#     wb.save(response)
#
#     # retorna a resposta
#     # linha obrigatória
#     # ou o sistema quebra
#     return response