from datetime import datetime
from django.utils.timezone import make_aware
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado
from areas.models_limpeza_predial import AreaLimpezaPredial
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial


def agendar_servicos_limpeza_predial_configurados():
    objects = ServicoLimpezaPredialConfigurado.objects.filter(
        status__in=['Mobilizado'],
        Areas__status__in=['Mobilizado'],
        Areas__localidade__status__in=['Mobilizado'],
        Areas__localidade__unidade__status__in=['Mobilizado']
    )

    # Mapeamento para dias em português
    dias_semana_portugues = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    for obj in objects:
        # Obter a área correspondente
        area = AreaLimpezaPredial.objects.get(id_random=obj.Areas.id_random)

        # Obter todos os serviços escalados do Catalogo
        ServicosEscalados = CatalogodeServicoLimpezaPredial.objects.filter(
            id_random__in=[servico.id_random for servico in obj.ServicosEscalados.all()]
        )
        idconfigurate = obj.id_random
        diasaseremrealizado = obj.diasaseremrealizado.all()
        tempomedioplanejado = obj.tempomedioplanejado
        horarios = [
            obj.horario_1, obj.horario_2, obj.horario_3, obj.horario_4,
            obj.horario_5, obj.horario_6, obj.horario_7,
        ]

        # Obtém o dia da semana atual
        dia_atual_semana = datetime.now().strftime('%A')

        # Validação se o dia atual está na lista de dias para realizar o serviço
        if dias_semana_portugues.get(dia_atual_semana) in [dia.diasdasemana for dia in diasaseremrealizado]:
            for horario in horarios:
                if horario:
                    # Combina a data atual com o horário especificado
                    data_atual = datetime.now().date()
                    data_inicio = make_aware(datetime.combine(data_atual, horario))

                    # Calcula a data de conclusão
                    data_conclusao = data_inicio + tempomedioplanejado

                    # Criação do novo objeto agendado
                    new_service_scheduled = ServicoLimpezaPredialAgendado(
                        id_configuracao=idconfigurate,
                        DescricaoDoServico=", ".join(
                            servicoescalado.nome
                            for servicoescalado in ServicosEscalados
                        )[:199],
                        Areas=area,
                        DataDeInicio=data_inicio,
                        DataDeConclusao=data_conclusao,
                        TipoServico='Automático'
                    )

                    # Salva o objeto de agendamento
                    new_service_scheduled.save()

                    # Adiciona todos os serviços escalados ao campo ManyToMany
                    new_service_scheduled.ServicosEscalados.set(ServicosEscalados)