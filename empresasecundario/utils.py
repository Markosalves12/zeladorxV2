from gerente.models import Gerente

def define_empresa_primaria_ids(request, userid):
    gerente = Gerente.objects.get(id_random=userid)
    empresas_primarias_ids = [
        empresa.empresaprimaria.id_random
        for empresa in gerente.empresasecundaria.all()
    ]

    return empresas_primarias_ids