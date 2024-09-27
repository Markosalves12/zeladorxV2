def classicate_login(request):
    nome = request.session.get('login_nome', '')
    # type = request.session.get('login_type', '')
    userid = request.session.get('userid', '')
    # empresa = request.session.get('empresa', '')
    # id_random_empresa = request.session.get('id_random_empresa', '')

    return {
        'nome': nome,
        # 'type': type,
        'userid': userid,
        # 'empresa': empresa,
        # 'id_random_empresa': id_random_empresa
    }