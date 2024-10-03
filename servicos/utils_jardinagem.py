from servicos.models_jardinagem import FatoServicoJardinagem, ServicoJardinagemAgendado
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateTimeField
                              )


def colect_dados_fato_servico_jardinagem(request, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, status=list):
    # Adicione os dados do relatório ao arquivo Excel
    filters = {
        'status_servico__in': status,
        'tipodeempresa': 'Jardinagem',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['data_de_inicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['data_de_conclusao__lte'] = DataDeConclusao

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['servicos_solicitados_id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['colaboradores_chamados_id__in'] = ColaboradoresEscalados

    dados = FatoServicoJardinagem.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__empresasecundaria__setor__setor'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('Servico__ServicosEscalados__EmpresaSecundaria__nome'),
            output_field=CharField()
        ),
        id_agendamento=ExpressionWrapper(
            F('Servico__id'),
            output_field=IntegerField()
        ),
        tipo_agendamento=ExpressionWrapper(
            F('Servico__TipoServico'),
            output_field=CharField()
        ),
        descricao_do_servico=ExpressionWrapper(
            F('Servico__DescricaoDoServico'),
            output_field=CharField()
        ),
        colaboradores_chamados=ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__username'),
            output_field=CharField()
        ),
        colaboradores_chamados_id=ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__id'),
            output_field=IntegerField()
        ),
        servicos_solicitados=ExpressionWrapper(
            F('Servico__ServicosEscalados__nome'),
            output_field=CharField()
        ),
        servicos_solicitados_id=ExpressionWrapper(
            F('Servico__ServicosEscalados__id'),
            output_field=IntegerField()
        ),
        data_de_inicio=ExpressionWrapper(
            F('Servico__DataDeInicio'),
            output_field=DateTimeField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('Servico__DataDeConclusao'),
            output_field=DateTimeField()
        ),
        antes=ExpressionWrapper(
            F('Servico__foto_solicitacao'),
            output_field=CharField()
        ),
        depois=ExpressionWrapper(
            F('Servico__foto_entrega'),
            output_field=CharField()
        ),
        status_servico=ExpressionWrapper(
            F('Servico__status'),
            output_field=CharField()
        ),
        area_atendida=ExpressionWrapper(
            F('Servico__Areas__nome'),
            output_field=CharField()
        ),
        area_atendid_id=ExpressionWrapper(
            F('Servico__Areas__id'),
            output_field=IntegerField()
        ),
        periodicidade_de_retorno=ExpressionWrapper(
            F('Servico__Areas__periodicidade'),
            output_field=CharField()
        ),
        area_total=ExpressionWrapper(
            F('Servico__Areas__dimensao'),
            output_field=CharField()
        ),
        tipo_vegetacao=ExpressionWrapper(
            F('Servico__Areas__vegetacao__nome'),
            output_field=CharField()
        ),
        tipo_terreno=ExpressionWrapper(
            F('Servico__Areas__Terreno__nome'),
            output_field=CharField()
        ),
        localidade=ExpressionWrapper(
            F('Servico__Areas__localidade__nome'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('Servico__Areas__localidade__unidade__nome'),
            output_field=CharField()
        ),
        id_servico=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        tempo_na_area=ExpressionWrapper(
            F('data_hora_retorno_area') - F('data_hora_chegada_na_area'),
            output_field=DurationField()
        ),
        colaborador_envolvido=ExpressionWrapper(
            F('Gerente__username'),
            output_field=CharField()
        ),
        colaborador_envolvido_id_random=ExpressionWrapper(
            F('Gerente__id_random'),
            output_field=CharField()
        ),
        data_hora_chegada=ExpressionWrapper(
            F('data_hora_chegada_na_area'),
            output_field=DateTimeField()
        ),
        data_hora_retorno=ExpressionWrapper(
            F('data_hora_retorno_area'),
            output_field=DateTimeField()
        ),
        id_random_area=ExpressionWrapper(
            F('Servico__Areas__id_random'),
            output_field=CharField()
        ),
        id_random_servico=ExpressionWrapper(
            F('Servico__ServicosEscalados__id_random'),
            output_field=CharField()
        ),
        id_random_configuracao=ExpressionWrapper(
            F('Servico__id_configuracao'),
            output_field=CharField()
        ),
        tipo_de_servico=ExpressionWrapper(
            F('Servico__TipoServico'),
            output_field=CharField()
        ),
    ).filter(
        **filters
    )

    return dados


def colect_dados_agendamentos_jardinagem(request, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, status=list):
    # Adicione os dados do relatório ao arquivo Excel
    filters = {
        'status_servico__in': status,
        'tipodeempresa': 'Jardinagem',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['data_de_inicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['data_de_conclusao__lte'] = DataDeConclusao

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['servicos_solicitados_id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['colaboradores_chamados_id__in'] = ColaboradoresEscalados

    dados = ServicoJardinagemAgendado.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('ColaboradoresEscalados__empresasecundaria__setor__setor'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('ServicosEscalados__EmpresaSecundaria__nome'),
            output_field=CharField()
        ),
        id_agendamento=ExpressionWrapper(
            F('id'),
            output_field=CharField()
        ),
        tipo_agendamento=ExpressionWrapper(
            F('TipoServico'),
            output_field=CharField()
        ),
        descricao_do_servico=ExpressionWrapper(
            F('DescricaoDoServico'),
            output_field=CharField()
        ),
        colaboradores_chamados=ExpressionWrapper(
            F('ColaboradoresEscalados__username'),
            output_field=CharField()
        ),
        colaboradores_chamados_id=ExpressionWrapper(
            F('ColaboradoresEscalados__id'),
            output_field=IntegerField()
        ),
        colaboradores_chamados_id_random=ExpressionWrapper(
            F('ColaboradoresEscalados__id_random'),
            output_field=IntegerField()
        ),
        servicos_solicitados=ExpressionWrapper(
            F('ServicosEscalados__nome'),
            output_field=CharField()
        ),
        servicos_solicitados_id=ExpressionWrapper(
            F('ServicosEscalados__id'),
            output_field=IntegerField()
        ),
        data_de_inicio=ExpressionWrapper(
            F('DataDeInicio'),
            output_field=DateTimeField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('DataDeConclusao'),
            output_field=DateTimeField()
        ),
        antes=ExpressionWrapper(
            F('foto_solicitacao'),
            output_field=CharField()
        ),
        depois=ExpressionWrapper(
            F('foto_entrega'),
            output_field=CharField()
        ),
        status_servico=ExpressionWrapper(
            F('status'),
            output_field=CharField()
        ),
        area_atendida=ExpressionWrapper(
            F('Areas__nome'),
            output_field=CharField()
        ),
        periodicidade_de_retorno=ExpressionWrapper(
            F('Areas__periodicidade'),
            output_field=CharField()
        ),
        area_total=ExpressionWrapper(
            F('Areas__dimensao'),
            output_field=CharField()
        ),
        tipo_vegetacao=ExpressionWrapper(
            F('Areas__vegetacao__nome'),
            output_field=CharField()
        ),
        tipo_terreno=ExpressionWrapper(
            F('Areas__Terreno__nome'),
            output_field=CharField()
        ),
        localidade=ExpressionWrapper(
            F('Areas__localidade__nome'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('Areas__localidade__unidade__nome'),
            output_field=CharField()
        ),
        id_random_area=ExpressionWrapper(
            F('Areas__id_random'),
            output_field=CharField()
        ),
        id_random_servico=ExpressionWrapper(
            F('id_random'),
            output_field=CharField()
        ),
    ).filter(
        **filters
    )

    return dados
