from empresasecundario.utils import define_empresas

def create_global_parameters(request):
    request.session['application'] = 'ZeladorX'
    application = request.session.get('application', '')

    return {
        'application': application
    }

def define_wallet(request):
    empresas = define_empresas(request=request, userid=request.session.get('userid', ''))
    setores = empresas['setores']
    em_parceria = empresas['em_parceria']
    habilitar_jardinagem = False
    habilitar_limpeza = False

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        habilitar_jardinagem = True

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        habilitar_limpeza = True

    return {
        'habilitar_jardinagem': habilitar_jardinagem,
        'habilitar_limpeza': habilitar_limpeza,
        'em_parceria': em_parceria
    }