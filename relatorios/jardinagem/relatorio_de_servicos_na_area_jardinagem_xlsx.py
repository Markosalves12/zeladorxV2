import openpyxl
from servicos.headers_report_jardinagem import headers_report_services
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem
from django.http import HttpResponse


def exportar_relatorio_de_serivos_na_area_Jardinagem_excel(request, userid, id_random):
    wb = openpyxl.Workbook()
    ws = wb.active

    # cabeçalhos da tabela exportada
    headers = headers_report_services

    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header_title

    # Adicione os dados do relatório ao arquivo Excel
    dados = colect_dados_fato_servico_jardinagem(
        request=request,
        status=['Concluido'],
    ).filter(
        id_random_area=id_random
    )

    for row_num, row in enumerate(dados, start=2):
        row_data = [
            row.tipodeempresa, row.empresaprestadora,

            row.id_servico, row.tipo_agendamento,

            row.descricao_do_servico, row.colaboradores_chamados, row.servicos_solicitados, row.data_de_inicio,

            row.data_de_conclusao, row.antes, row.depois, row.status_servico,

            row.area_atendida, row.periodicidade_de_retorno,

            row.area_total, row.tipo_vegetacao, row.tipo_terreno, row.localidade,
            # row.tiponegocio,
            row.unidade,

            row.id_servico, row.tempo_na_area, row.colaborador_envolvido,
            # row.principalservico,
            row.data_hora_chegada, row.data_hora_retorno
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
    response['Content-Disposition'] = 'attachment; filename="relatorio de servicos.xlsx"'

    # Salve o arquivo Excel
    wb.save(response)

    # retorna a resposta
    # linha obrigatória
    # ou o sistema quebra
    return response