from gerente.models import Gerente

def define_empresas(request, userid):
    gerente = Gerente.objects.get(id_random=userid)

    # IDs das empresas primárias
    empresas_primarias_ids = [
        empresa.empresaprimaria.id_random
        for empresa in gerente.empresasecundaria.all()
    ]

    # IDs das empresas secundárias
    empresas_secundarias_ids = [
        empresa.id_random
        for empresa in gerente.empresasecundaria.all()
    ]

    return {
        'empresas_primarias_ids': empresas_primarias_ids,
        'empresas_secundarias_ids': empresas_secundarias_ids
    }