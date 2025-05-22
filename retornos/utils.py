from datetime import timedelta

def formatar_tempo_desde(duracao: timedelta):
    if not duracao:
        return "Desconhecido"

    dias = duracao.days

    if dias < 30:
        return f"{dias} dias"
    elif dias < 365:
        meses = int(dias // 30.5)
        dias_restantes = int(dias % 30.5)
        if meses == 1:
            return f"{meses} mês e {dias_restantes} dias"
        return f"{meses} meses e {dias_restantes} dias"
    else:
        meses = int(dias // 30.5)
        dias_restantes = int(dias % 30.5)
        return f"{meses} meses e {dias_restantes} dias"