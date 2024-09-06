from django.shortcuts import render, redirect
from authenticate.forms import LoginForms
from django.contrib import auth
from django.contrib.auth.models import User
# from gestor.models import Gestor
from gerente.models import Gerente
from django.contrib.auth.hashers import check_password

# Create your views here.
def login(request):
    forms = LoginForms()
    if request.method == "POST":
        forms = LoginForms(request.POST)
        if forms.is_valid():
            email = forms['email'].value()
            senha = forms['senha'].value()

            try:
                print(email)
                print("gerente")
                gerente = Gerente.objects.get(
                    email=email
                )
                print(gerente)
                print(email)

                if check_password(senha, gerente.password) and gerente.status == "Mobilizado":
                    print("acesado")
                    # request.session['login_nome'] = gerente.username
                    request.session['userid'] = gerente.id_random
                    # request.session['empresa'] = f'{gerente.EmpresaSecundaria.nome}'
                    # request.session['id_random_empresa'] = f'{gerente.EmpresaSecundaria.id_random}'

                    return redirect('calendario_jardinagem', gerente.id_random)

            except:
                pass

    return render(
        request=request,
        template_name='authenticate/login.html',
        context={
           'forms': forms
        }
    )


def logout(request):
    # nome = get_random_string(10)
    # type = get_random_string(10)
    # id = get_random_string(10)
    #
    # request.session['login_nome'] = nome
    # request.session['login_type'] = type
    # request.session['login_id'] = id
    #
    return redirect('login')