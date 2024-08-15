from django.shortcuts import render

# Create your views here.
def dashboard_produtividade(request):
    return render(
        request=request,
        template_name='dashboards/dashboard_produtividade.html',
        context={
            'app_name': 'Dashboard produtividade'
        }
    )