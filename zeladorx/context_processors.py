def create_global_parameters(request):
    request.session['application'] = 'ZeladorX'
    application = request.session.get('application', '')

    return {
        'application': application
    }