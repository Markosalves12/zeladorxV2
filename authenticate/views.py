from django.shortcuts import render, redirect
from authenticate.forms import LoginForms
from django.contrib import auth
from django.contrib.auth.models import User
from gestor.models import Gestor
from gerente.models import Gerente
from colaborador.models import Colaborador
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
                usuario = User.objects.get(
                    email=email
                )

                usuario = auth.authenticate(
                    request,
                    username=usuario,
                    password=senha,
                )

                if usuario is not None:
                    auth.login(request, usuario)
                    return redirect('calendario')

            except:
                pass


            try:
                print(email)
                print("gestor")
                gestor = Gestor.objects.get(
                    email=email
                )
                print(gestor.password)
                if check_password(senha, gestor.password) and gestor.status == "Mobilizado":
                    request.session['login_nome'] = gestor.username
                    request.session['login_type'] = 'Gestor'
                    request.session['login_id'] = gestor.id_random
                    request.session['empresa'] = f'{gestor.EmpresaSecundaria.nome}'
                    request.session['id_random_empresa'] = f'{gestor.EmpresaSecundaria.id_random}'
                    return redirect('calendario')

            except:
                pass


            try:
                print(email)
                print("gerente")
                gerente = Gerente.objects.get(
                    email=email
                )
                print(gerente)
                print(gerente.password)
                if check_password(senha, gerente.password) and gerente.status == "Mobilizado":
                    request.session['login_nome'] = gerente.username
                    request.session['login_type'] = 'Gerente'
                    request.session['login_id'] = gerente.id_random
                    request.session['empresa'] = f'{gerente.gestor.EmpresaSecundaria.nome}'
                    request.session['id_random_empresa'] = f'{gerente.gestor.EmpresaSecundaria.id_random}'
                    return redirect('calendario')

            except:
                pass


            try:
                print(email)
                print("colaborador")

                colaborador = Colaborador.objects.get(
                    email=email
                )
                print(colaborador.password)
                if check_password(senha, colaborador.password) and colaborador.status == "Mobilizado":
                    request.session['login_nome'] = colaborador.username
                    request.session['login_type'] = 'Colaborador'
                    request.session['login_id'] = colaborador.id_random
                    request.session['empresa'] = f'{colaborador.gerente.gestor.EmpresaSecundaria.nome}'
                    request.session['id_random_empresa'] = f'{colaborador.gerente.gestor.EmpresaSecundaria.id_random}'
                    return redirect('calendario')
                else:
                    pass

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