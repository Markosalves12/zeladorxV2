import openpyxl
from servicos.headers_report_jardinagem import headers_report_services, headers_report_schedules
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem, colect_dados_agendamentos_jardinagem
from django.http import HttpResponse
from utils.utils import generate_id_random
from datetime import datetime
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect

def exportar_relatorio_de_serivos_Jardinagem_excel(
    request, userid, status, DataDeInicio, DataDeConclusao, Areas,
    TipoServico, ServicosEscalados, ColaboradoresEscalados
):
    # Verifica login
    block = verify_login(request=request, userid=userid)
    if block:
        return redirect('logout')

    # Configuração inicial do workbook
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

    # Seleciona cabeçalhos e coleta dados
    if 'Concluido' in status.split(','):
        headers = headers_report_services
        dados = colect_dados_fato_servico_jardinagem(
            request=request,
            userid=userid,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            ColaboradoresEscalados=ColaboradoresEscalados,
            TipoServico=TipoServico,
            Areas=Areas,
            status=status.split(',')
        )
    else:
        headers = headers_report_schedules
        dados = colect_dados_agendamentos_jardinagem(
            request=request,
            userid=userid,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            ColaboradoresEscalados=ColaboradoresEscalados,
            TipoServico=TipoServico,
            Areas=Areas,
            status=status.split(',')
        )

    # Adiciona os cabeçalhos ao Excel
    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header_title

    # Adiciona os dados ao Excel
    for row_num, row in enumerate(dados, start=2):
        row_data = [
            row.tipodeempresa, row.empresaprestadora,
            row.id_agendamento, row.tipo_agendamento,
            row.descricao_do_servico, row.colaboradores_chamados,
            row.servicos_solicitados,
            row.data_de_inicio.replace(tzinfo=None) if row.data_de_inicio else None,
            row.data_de_conclusao.replace(tzinfo=None) if row.data_de_conclusao else None,
            row.antes, row.depois, row.status_servico, row.area_atendida,
            row.id_random_area, row.periodicidade_de_retorno, row.area_total,
            row.tipo_vegetacao, row.tipo_terreno, row.localidade, row.unidade,
            row.id_servico, row.tempo_na_area, row.colaborador_envolvido,
            row.colaborador_envolvido_id_random,
            row.data_hora_chegada.replace(tzinfo=None) if row.data_hora_chegada else None,
            row.data_hora_retorno.replace(tzinfo=None) if row.data_hora_retorno else None
        ]
        for col_num, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="relatorio_de_servicos_{status}_{generate_id_random()}.xlsx"'

    # Salva o Excel na resposta
    wb.save(response)

    return response

# def exportar_relatorio_de_serivos_Jardinagem_excel(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
#                                                    TipoServico, ServicosEscalados, ColaboradoresEscalados):
#     block = verify_login(request=request, userid=userid)
#
#     if block == True:
#         return redirect('logout')
#
#     wb = openpyxl.Workbook()
#     ws = wb.active
#
#     DataDeInicio = datetime.strptime(DataDeInicio,
#                                      '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else None
#     DataDeConclusao = datetime.strptime(DataDeConclusao,
#                                         '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else None
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
#         dados = colect_dados_fato_servico_jardinagem(
#             request=request,
#             userid=userid,
#             DataDeInicio=DataDeInicio,
#             DataDeConclusao=DataDeConclusao,
#             ServicosEscalados=ServicosEscalados,
#             ColaboradoresEscalados=ColaboradoresEscalados,
#             TipoServico=TipoServico,
#             Areas=Areas,
#             status=status.split(',')
#         )
#
#         # Adicione os dados do relatório ao arquivo Excel
#         for row_num, row in enumerate(dados, start=2):
#             row_data = [
#                 row.tipodeempresa, row.empresaprestadora,
#                 row.id_agendamento, row.tipo_agendamento,
#                 row.descricao_do_servico, row.colaboradores_chamados,
#                 row.servicos_solicitados,
#                 row.data_de_inicio.replace(tzinfo=None) if row.data_de_inicio else None,  # Remove tzinfo
#                 row.data_de_conclusao.replace(tzinfo=None) if row.data_de_conclusao else None,  # Remove tzinfo
#                 row.antes, row.depois, row.status_servico, row.area_atendida, row.id_random_area,
#                 row.periodicidade_de_retorno, row.area_total, row.tipo_vegetacao, row.tipo_terreno,
#                 row.localidade, row.unidade, row.id_servico, row.tempo_na_area, row.colaborador_envolvido,
#                 row.colaborador_envolvido_id_random,
#                 row.data_hora_chegada.replace(tzinfo=None) if row.data_hora_chegada else None,  # Remove tzinfo
#                 row.data_hora_retorno.replace(tzinfo=None) if row.data_hora_retorno else None,  # Remove tzinfo
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
#         headers = headers_report_schedules
#
#         for col_num, header_title in enumerate(headers, 1):
#             cell = ws.cell(row=1, column=col_num)
#             cell.value = header_title
#
#         dados = colect_dados_agendamentos_jardinagem(
#             request=request,
#             userid=userid,
#             DataDeInicio=DataDeInicio,
#             DataDeConclusao=DataDeConclusao,
#             ServicosEscalados=ServicosEscalados,
#             ColaboradoresEscalados=ColaboradoresEscalados,
#             TipoServico=TipoServico,
#             Areas=Areas,
#             status=status.split(',')
#         )
#
#         for row_num, row in enumerate(dados, start=2):
#             row_data = [
#                 row.tipodeempresa, row.empresaprestadora,
#
#                 row.id_agendamento, row.tipo_agendamento,
#
#                 row.descricao_do_servico, row.colaboradores_chamados,
#
#                 row.servicos_solicitados, row.data_de_inicio, row.data_de_conclusao,
#
#                 row.antes, row.depois, row.status_servico, row.area_atendida,
#
#                 row.periodicidade_de_retorno, row.area_total, row.tipo_vegetacao, row.tipo_terreno,
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