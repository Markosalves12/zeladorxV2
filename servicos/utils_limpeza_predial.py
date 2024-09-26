from servicos.models_limpeza_predial import FatoServicoLimpezaPredial
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateField, DateTimeField, Value
                              )
from django.db.models.functions import Concat
from django.conf import settings

def colect_dados_fato_servico_limpeza_predial(request, status=list):
    dados = FatoServicoLimpezaPredial.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('Servico__ServicosEscalados__EmpresaSecundaria__setor'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('Servico__ServicosEscalados__EmpresaSecundaria__nome'),
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
        servicos_solicitados=ExpressionWrapper(
            F('Servico__ServicosEscalados__nome'),
            output_field=CharField()
        ),
        data_de_inicio=ExpressionWrapper(
            F('Servico__DataDeInicio'),
            output_field=DateTimeField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('Servico__DataDeConclusao'),
            output_field=DateTimeField()
        ),
        tempo_na_area=ExpressionWrapper(
            F('data_hora_retorno_area') - F('data_hora_chegada_na_area'),
            output_field=DurationField()
        ),
        colaborador_envolvido=ExpressionWrapper(
            F('Gerente__username'),
            output_field=CharField()
        ),
        area_atendida=ExpressionWrapper(
            F('Servico__Areas'),
            output_field=CharField()
        ),
        area_atendida_dimensao=ExpressionWrapper(
            F('Servico__Areas__dimensao'),
            output_field=CharField()
        ),
        foto_conclusao=ExpressionWrapper(
            F('foto_entrega'),
            output_field=CharField()
        ),
        id_random_area=ExpressionWrapper(
            F('Servico__Areas__id_random'),
            output_field=CharField()
        ),
    ).filter(
        Servico__status__in=status
    )

    return dados