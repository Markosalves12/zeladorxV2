from servicos.models_limpeza_predial import FatoServicoLimpezaPredial, ServicoLimpezaPredialAgendado
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateTimeField
                              )
from empresasecundario.utils import define_empresas

def colect_dados_fato_servico_limpeza_predial(request, userid, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, TipoServico, Areas, status=list):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    filters = {
        'status_servico__in': status,
        'tipodeempresa': 'Limpeza predial',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['data_de_inicio__gte'] = DataDeInicio

    if TipoServico and TipoServico != "None":
        filters['tipo_de_servico'] = TipoServico

    if DataDeConclusao and DataDeConclusao != "None":
        filters['data_de_conclusao__lte'] = DataDeConclusao

    if Areas and Areas != "None":
        filters['area_atendid_id'] = Areas

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['servicos_solicitados_id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['colaboradores_chamados_id__in'] = ColaboradoresEscalados

    dados = FatoServicoLimpezaPredial.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('Servico__ServicosEscalados__EmpresaSecundaria__setor__setor'),
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
        area_total=ExpressionWrapper(
            F('Servico__Areas__dimensao'),
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
        foto_conclusao=ExpressionWrapper(
            F('foto_entrega'),
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
        **filters,
        Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Servico__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
    )

    return dados

def colect_dados_agendamentos_limpeza_predial(request, userid, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, TipoServico, Areas, status=list):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    filters = {
        'status_servico__in': status,
        'tipodeempresa': 'Limpeza predial',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['data_de_inicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['data_de_conclusao__lte'] = DataDeConclusao

    if Areas and Areas != "None":
        filters['area_atendid_id'] = Areas

    if TipoServico and TipoServico != "None":
        filters['tipo_agendamento'] = TipoServico

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['servicos_solicitados_id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['colaboradores_chamados_id__in'] = ColaboradoresEscalados

    dados = ServicoLimpezaPredialAgendado.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('ServicosEscalados__EmpresaSecundaria__setor__setor'),
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
        servicos_solicitados=ExpressionWrapper(
            F('ServicosEscalados__nome'),
            output_field=CharField()
        ),
        servicos_solicitados_id=ExpressionWrapper(
            F('ServicosEscalados__nome'),
            output_field=CharField()
        ),
        data_de_inicio=ExpressionWrapper(
            F('DataDeInicio'),
            output_field=DateTimeField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('DataDeConclusao'),
            output_field=DateTimeField()
        ),
        status_servico=ExpressionWrapper(
            F('status'),
            output_field=CharField()
        ),
        area_atendida=ExpressionWrapper(
            F('Areas__nome'),
            output_field=CharField()
        ),
        area_atendid_id=ExpressionWrapper(
            F('Areas__id'),
            output_field=CharField()
        ),
        area_total=ExpressionWrapper(
            F('Areas__dimensao'),
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
        **filters,
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
    )

    return dados