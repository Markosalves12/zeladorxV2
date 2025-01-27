from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from servicos.models_jardinagem import ServicoJardinagemAgendado, ServicoJardinagemConfigurado
from areas.models_jardinagem import AreasJardins
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from gerente.models import Gerente


def agendar_servicos_jardinagem_configurados():
    objects = ServicoJardinagemConfigurado.objects.filter(
        status='Mobilizado',
        Areas__status='Mobilizado',
        Areas__localidade__status='Mobilizado',
        Areas__localidade__unidade__status='Mobilizado'
    )

    dias_semana_portugues = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    dia_atual_semana = datetime.now().strftime('%A')

    # Define o gerente padrão
    gerente_padrao = Gerente.objects.filter(id_random='MuUe1D3pvT3v').first()

    for obj in objects:
        try:
            area = AreasJardins.objects.get(id_random=obj.Areas.id_random)
        except AreasJardins.DoesNotExist:
            print(f"Área com id_random {obj.Areas.id_random} não encontrada. Pulando...")
            continue

        ServicosEscalados = CatalogodeServicoJardinagem.objects.filter(
            id_random__in=[servico.id_random for servico in obj.ServicosEscalados.all()],
            status='Mobilizado'
        )

        if not ServicosEscalados.exists():
            print(f"Objeto {obj.id_random} não possui serviços escalados mobilizados. Pulando...")
            continue

        idconfigurate = obj.id_random
        diasaseremrealizado = obj.diasaseremrealizado.all()
        tempomedioplanejado = obj.tempomedioplanejado or timedelta(minutes=30)

        horarios = [h for h in [
            obj.horario_1, obj.horario_2, obj.horario_3,
            obj.horario_4, obj.horario_5, obj.horario_6, obj.horario_7
        ] if h]

        if not horarios:
            print(f"Objeto {obj.id_random} não possui horários válidos. Pulando...")
            continue

        if dias_semana_portugues.get(dia_atual_semana) not in [dia.diasdasemana for dia in diasaseremrealizado]:
            continue

        for horario in horarios:
            data_atual = datetime.now().date()
            data_inicio = make_aware(datetime.combine(data_atual, horario))
            data_conclusao = data_inicio + tempomedioplanejado

            new_service_scheduled = ServicoJardinagemAgendado(
                id_configuracao=idconfigurate,
                DescricaoDoServico=", ".join(servicoescalado.nome for servicoescalado in ServicosEscalados)[:199],
                Areas=area,
                DataDeInicio=data_inicio,
                DataDeConclusao=data_conclusao,
                TipoServico='Automático',
            )

            new_service_scheduled.save()
            new_service_scheduled.ServicosEscalados.set(ServicosEscalados)

            if gerente_padrao:
                new_service_scheduled.ColaboradoresEscalados.set([gerente_padrao])

            print(f"Serviço de jardinagem agendado para {data_inicio} na área {area.id_random}")