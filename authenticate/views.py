from django.shortcuts import render, redirect
from authenticate.forms import LoginForms
from gerente.models import Gerente
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from dotenv import load_dotenv
import os

load_dotenv()


# Create your views here.
def login(request):
    forms = LoginForms()
    if request.method == "POST":
        forms = LoginForms(request.POST)
        if forms.is_valid():

            email = forms['email'].value()
            senha = forms['senha'].value()

            print(email,'\n', senha)

            try:
                gerente = Gerente.objects.get(
                    email=email
                )

                usuario = User.objects.get(
                    email=email
                )

                usuario = auth.authenticate(
                    request,
                    username=usuario,
                    password=str(os.getenv('DEFAULT_PASSWORD')),
                )

                if usuario is not None:
                    auth.login(request, usuario)
                    # messages.success(request, f"{nome} logado com sucesso")
                    print("logado")
                else:
                    print("Rejeitado")


                print('222')
                if check_password(senha, gerente.password) and gerente.status == "Mobilizado":
                    request.session['login_nome'] = gerente.username
                    request.session['userid'] = gerente.id_random

                    auth.login(request, usuario)

                    return redirect('calendario_jardinagem', gerente.id_random)
                print('eeeee')
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
    auth.logout(request)
    request.session['login_nome'] = ''
    request.session['userid'] = str(os.getenv('ID_RANDOM_DEFAULT_USER'))
    messages.success(request, "Logout efetuado com sucesso")

    return redirect('login')
