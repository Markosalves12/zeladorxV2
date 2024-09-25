import openpyxl
from servicos.headers_report_jardinagem import headers_report_services
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem
from django.http import HttpResponse


def exportar_relatorio_de_serivos_limpeza_predial_excel(request, userid, status):
    wb = openpyxl.Workbook()
    ws = wb.active

    # cabeçalhos da tabela exportada
    headers = headers_report_services

    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header_title

    print(status.split(','))
    print(type(status.split(',')))

    # Adicione os dados do relatório ao arquivo Excel
    dados = colect_dados_fato_servico_jardinagem(
        request=request,
        status=status.split(',')
    )

    for row_num, row in enumerate(dados, start=2):
        row_data = [
            row.tipodeempresa, row.empresaprestadora,

            row.id_servico, row.tipo_agendamento,

            row.descricao_do_servico, row.colaboradores_chamados, row.servicos_solicitados, row.data_de_inicio,

            row.data_de_conclusao, row.antes, row.depois, row.status_servico,

            # row.equipamento_marca,
            row.equipamento_catalogo, row.equipamento_empresa, row.tipo_equipamento, row.equipamento_id,
            # row.vida_util_equipamento,
            row.data_aquisicao_equipamento, row.data_desmobilizacao_equipamento, row.matricula_equipamento,

            # row.ferramenta_marca, row.ferramenta_catalogo, row.ferramenta_empresa, row.tipo_ferramenta, row.ferramenta_id, row.vida_util_ferramenta, row.data_aquisicao_ferramenta, row.data_desmobilizacao_ferramenta, row.matricula_ferramenta,

            # row.material_aplicado, row.material_categoria, row.forma_consumo, row.qtd, row.tipo_material,

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