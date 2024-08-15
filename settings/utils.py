from django.shortcuts import get_object_or_404
from gestor.forms import GestorForms
from gerente.forms import GerenteForms
from colaborador.forms import ColaboradorForms
from settings.models import SettingServicosGerente, SettingServicosGestor, SettingServicosColaborador


def define_setting(request, model_class, form_class, email):
    objeto = get_object_or_404(model_class, email=email)
    print(objeto)
    if form_class == GestorForms:
        setting = SettingServicosGestor(Gestor=objeto)
        setting.save()
        print("Configuracao gestor")

    elif form_class == GerenteForms:
        setting = SettingServicosGerente(Gerente=objeto)
        setting.save()
        print("Configuracao gerente")

    elif form_class == ColaboradorForms:
        setting = SettingServicosColaborador(Colaborador=objeto)
        setting.save()
        print("Configuracao colaborador")

    else:
        print("Não achei")