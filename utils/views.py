from django.shortcuts import render, redirect, get_object_or_404
from utils.utils import DataTableAndForms
from django.urls import reverse
from settings.utils import define_setting
from permissionscontrol.utils import configurate_permissions
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsAccessLimpezaPredial
from empresasecundario.forms import EmpresaSecundariaForms

def generic_view(request, model, form_class, template_name, columns, edition_rout, app_name,
                 text_button_open_modal, text_button_save,  header_model,
                 redirect_url, userid=False, button_export_tittle=False, button_export_link=False,
                 link_tipos=None, modal_button=True, configurate_gerente=False, history_rout=False,
                 permission_view=True, permission_edit=True, permission_crate=True):

    dt_and_forms = DataTableAndForms(
        request=request,
        model=model,
        modelforms=form_class,
        per_page=15,
        columns=columns,
        edition_rout=edition_rout,
        history_rout=history_rout,
        userid=userid
    )

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            if configurate_gerente:
                email = form.cleaned_data['email']
                form.save()

                define_setting(
                    request=request,
                    model_class=model,
                    form_class=form_class,
                    email=email
                )

                configurate_permissions(
                    request=request,
                    model_class=model,
                    email=email
                )

                return redirect(redirect_url, request.session.get('userid', ''))

            else:
                form.save()
                return redirect(redirect_url, request.session.get('userid', ''))

    forms, dados_paginados = dt_and_forms.get_data_and_forms()

    url_action = reverse(redirect_url, kwargs={'userid': request.session.get('userid', '')})

    return render(
        request=request,
        template_name=template_name,
        context={
            'dados_paginados': dados_paginados,
            'forms': forms,
            'app_name': f'{app_name.capitalize()}',
            'colunas': columns,
            'text_button_open_modal': f'{text_button_open_modal.lower()}',
            'text_button_save': f'{text_button_save.lower()}',
            'header_model': f'{header_model.lower()}',
            'url_action': url_action,
            'button_export_tittle': button_export_tittle,
            'button_export_link': button_export_link,
            'link_tipos': link_tipos,
            'modal_button': modal_button,
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate
        }
    )


def edit_generic_view(request, model_class, form_class, template_name, id_random, app_name, redirect_url_name,
                      redirect_close_button, link_tipos=None, permission_edit=True):

    objeto = get_object_or_404(model_class, id_random=id_random)

    forms = form_class(instance=objeto, request=request, userid=request.session.get('userid', ''))

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=objeto, request=request, userid=request.session.get('userid', '') )
        print(form.errors)

        if form.is_valid():
            form.save()
            return redirect(reverse(redirect_url_name, kwargs={'userid': request.session.get('userid', ''), 'id_random':id_random}))

    return render(
        request=request,
        template_name=template_name,
        context={
            'forms': forms,
            'app_name': app_name,
            'id_random': id_random,
            'text_button': 'Salvar',
            'redirect_url_name': redirect_url_name,
            'redirect_close_button': redirect_close_button,
            'permission_edit': permission_edit,
            'link_tipos': link_tipos
        }
    )