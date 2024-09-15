from django.shortcuts import get_object_or_404
from gerente.forms_jardinagem import GerenteJardinagemForms
from settings.models import SettingServicosGerente


def define_setting(request, model_class, form_class, email):
    objeto = get_object_or_404(model_class, email=email)
    print(objeto)

    if form_class == GerenteJardinagemForms:
        setting = SettingServicosGerente(Gerente=objeto)
        setting.save()
        print("Configuracao gerente")

    else:
        print("Não achei")