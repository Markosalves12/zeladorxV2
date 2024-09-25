from servicos.models_jardinagem import FatoServicoJardinagem
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateField, DateTimeField
                              )

def colect_dados_fato_servico_jardinagem(request, status=list):
    # Adicione os dados do relatório ao arquivo Excel
    dados = FatoServicoJardinagem.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__empresasecundaria__setor'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__empresasecundaria__nome'),
            output_field=CharField()
        ),
        id_agendamento=ExpressionWrapper(
            F('Servico__id'),
            output_field=CharField()
        ),
        tipo_agendamento=ExpressionWrapper(
            F('Servico__TipoServico'),
            output_field=CharField()
        ),
        descricao_do_servico=ExpressionWrapper(
            F('Servico__DescricaoDoServico'),
            output_field=CharField()
        ),
        colaboradores_chamados = ExpressionWrapper(
            F('Servico__ColaboradoresEscalados__username'),
            output_field=CharField()
        ),
        servicos_solicitados=ExpressionWrapper(
            F('Servico__ServicosEscalados__nome'),
            output_field=CharField()
        ),
        data_de_inicio=ExpressionWrapper(
            F('Servico__DataDeInicio'),
            output_field=CharField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('Servico__DataDeConclusao'),
            output_field=CharField()
        ),
        antes=ExpressionWrapper(
            F('Servico__foto_solicitacao'),
            output_field=CharField()
        ),
        depois=ExpressionWrapper(
            F('Servico__foto_entrega'),
            output_field=CharField()
        ),
        equipamento_catalogo=ExpressionWrapper(
            F('EquipamentoUsado__Nome'),
            output_field=CharField()
        ),
        equipamento_empresa=ExpressionWrapper(
            F('EquipamentoUsado__EmpresaSecundaria__nome'),
            output_field=CharField()
        ),
        tipo_equipamento=ExpressionWrapper(
            F('EquipamentoUsado__tipoequipamento'),
            output_field=CharField()
        ),
        equipamento_id=ExpressionWrapper(
            F('EquipamentoUsado__id'),
            output_field=CharField()
        ),
        data_aquisicao_equipamento=ExpressionWrapper(
            F('EquipamentoUsado__DataDeAquisicao'),
            output_field=DateField()
        ),
        data_desmobilizacao_equipamento=ExpressionWrapper(
            F('EquipamentoUsado__DataDeDesmobilizacao'),
            output_field=DateField()
        ),
        matricula_equipamento=ExpressionWrapper(
            F('EquipamentoUsado__matricula'),
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
        periodicidade_de_retorno=ExpressionWrapper(
            F('Servico__Areas__periodicidade'),
            output_field=CharField()
        ),
        area_total=ExpressionWrapper(
            F('Servico__Areas__dimensao'),
            output_field=CharField()
        ),
        tipo_vegetacao = ExpressionWrapper(
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

        tempo_na_area = ExpressionWrapper(
                F('data_hora_retorno_area')-F('data_hora_chegada_na_area'),
                output_field=DurationField()
        ),
        colaborador_envolvido=ExpressionWrapper(
            F('Gerente__username'),
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
    ).filter(
        Servico__status__in=status
    )

    return dados