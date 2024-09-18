from datetime import datetime
from django.utils.timezone import make_aware
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado


def agendar_servicos_limpeza_predial_configurados():
    objects = ServicoLimpezaPredialConfigurado.objects.all()

    for obj in objects:
        area = obj.area
        ServicosEscalados = obj.ServicosEscalados.all()
        diasaseremrealizado = obj.diasaseremrealizado.all()
        tempomedioplanejado = obj.tempomedioplanejado
        horarios = [
            obj.horario_1, obj.horario_2, obj.horario_3, obj.horario_4,
            obj.horario_5, obj.horario_6, obj.horario_7, obj.horario_8, obj.horario_9
        ]

        # Obtém o dia da semana atual
        dia_atual_semana = datetime.now().strftime('%A')  # Retorna o dia em inglês (ex.: 'Monday')

        # Mapeamento para dias em português (ajuste conforme necessário)
        dias_semana_portugues = {
            'Monday': 'Segunda-Feira',
            'Tuesday': 'Terça-Feira',
            'Wednesday': 'Quarta-Feira',
            'Thursday': 'Quinta-Feira',
            'Friday': 'Sexta-Feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }

        # Validação se o dia atual está na lista de dias para realizar o serviço
        if dias_semana_portugues[dia_atual_semana] in [dia.nome for dia in diasaseremrealizado]:
            for horario in horarios:
                if horario is not None:
                    # Combina a data atual com o horário especificado
                    data_atual = datetime.now().date()
                    data_inicio = make_aware(datetime.combine(data_atual, horario))

                    # Calcula a data de conclusão
                    data_conclusao = data_inicio + tempomedioplanejado

                    # Cria um novo agendamento
                    new_service_scheduled = ServicoLimpezaPredialAgendado(
                        DescricaoDoServico=", ".join(servicoescalado.nome for servicoescalado in ServicosEscalados)[
                                           :199],
                        area=area,
                        ServicosEscalados=ServicosEscalados,
                        DataDeInicio=data_inicio,
                        DataDeConclusao=data_conclusao,
                    )

                    new_service_scheduled.save()