from empresaprimaria.models import EmpresaPrimaria
from empresasecundario.models import EmpresaSecundaria
from zeladorx.models import TypeZeladoria
from gerente.models import Gerente

def define_empresas(request, userid):
    gerente = Gerente.objects.get(id_random=userid)

    # IDs das empresas primárias e secundárias
    empresas_primarias_ids = [
        empresa.empresaprimaria.id_random
        for empresa in gerente.empresasecundaria.all()
    ]

    empresas_secundarias_ids = [
        empresa.id_random
        for empresa in gerente.empresasecundaria.all()
    ]

    # Setores da empresa primária
    empresa_primaria = EmpresaPrimaria.objects.get(id_random=empresas_primarias_ids[0])
    setores_primaria = empresa_primaria.setor.all()  # Acessando o campo de chave estrangeira
    em_parceria = empresa_primaria.nome

    # Flags para habilitar campos da empresa primária
    habilitar_jardinagem = False
    habilitar_limpeza = False

    # Flags para habilitar campos da empresa secundária
    habilitar_jardinagem_secundaria = False
    habilitar_limpeza_secundaria = False

    # Checar os setores da empresa primária para definir as flags
    for objeto in TypeZeladoria.objects.filter(id__in=setores_primaria):
        if 'Jardinagem' in objeto.setor:
            habilitar_jardinagem = True
            # Definir permissão secundária se superuser for True
            if gerente.superuser:
                habilitar_jardinagem_secundaria = True

        if 'Limpeza predial' in objeto.setor:
            habilitar_limpeza = True
            # Definir permissão secundária se superuser for True
            if gerente.superuser:
                habilitar_limpeza_secundaria = True

    # Setores das empresas secundárias
    setores_secundarias = []
    for empresa_secundaria in EmpresaSecundaria.objects.filter(id_random__in=empresas_secundarias_ids):
        # Acessar setores associados à empresa secundária
        setores = empresa_secundaria.setor.all()
        setores_secundarias.extend(setores)

        # Verificar se algum setor da empresa secundária é jardinagem ou limpeza
        for objeto in TypeZeladoria.objects.filter(id__in=setores):
            if 'Jardinagem' in objeto.setor:
                habilitar_jardinagem_secundaria = True
            if 'Limpeza predial' in objeto.setor:
                habilitar_limpeza_secundaria = True

    # Retornar as informações das empresas e setores
    return {
        'empresas_primarias_ids': empresas_primarias_ids,
        'empresas_secundarias_ids': empresas_secundarias_ids,
        'em_parceria': em_parceria,
        'setores': {
            'habilitar_jardinagem': habilitar_jardinagem,
            'habilitar_limpeza': habilitar_limpeza,
            'habilitar_jardinagem_secundaria': habilitar_jardinagem_secundaria,
            'habilitar_limpeza_secundaria': habilitar_limpeza_secundaria,
            'setores_primaria': setores_primaria,
            'setores_secundarias': setores_secundarias,
        }
    }
