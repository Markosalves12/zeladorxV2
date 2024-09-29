from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models import F, ExpressionWrapper, IntegerField
from django.db.models.functions import Now
from empresasecundario.utils import define_empresas

def colect_dados_jardinagem(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    dados = ServicoJardinagemAgendado.objects.all().annotate(
        data_atual=Now(),
        status_agendamento=ExpressionWrapper(
            F('DataDeInicio') - F('data_atual'),
            output_field=IntegerField()
        ) / (3600 * 24 * 1000000)
    ).filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
    )

    return dados