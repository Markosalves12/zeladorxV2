from django.shortcuts import render, redirect
from authenticate.forms import LoginForms
from gerente.models import Gerente
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib import auth
from dotenv import load_dotenv
import os

load_dotenv()


# Create your views here.
def login(request):
    forms = LoginForms()
    if request.method == "POST":
        forms = LoginForms(request.POST)
        if forms.is_valid():

            email = forms.cleaned_data['email'].strip().lower()
            senha = forms.cleaned_data['senha']

            try:
                gerente = Gerente.objects.get(
                    email=email
                )

                usuario = auth.authenticate(
                    request,
                    username=str(os.getenv('DEFAULT_USER')),
                    password=str(os.getenv('DEFAULT_PASSWORD')),
                )

                if check_password(senha, gerente.password) and gerente.status == "Mobilizado":
                    request.session['login_nome'] = gerente.username
                    request.session['userid'] = gerente.id_random

                    auth.login(request, usuario)

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
    auth.logout(request)
    messages.success(request, "Logout efetuado com sucesso")

    return redirect('login')
