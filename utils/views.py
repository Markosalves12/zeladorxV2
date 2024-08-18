from django.shortcuts import render, redirect, get_object_or_404
from utils.utils import DataTableAndForms
from django.urls import reverse
from settings.utils import define_setting

def generic_view(request, model, form_class, template_name, columns, edition_rout, app_name,
                 text_button_open_modal, text_button_save,  header_model,
                 redirect_url, button_export_tittle=False, button_export_link=False,
                 link_tipos=None, modal_button=True):
    dt_and_forms = DataTableAndForms(
        request=request,
        model=model,
        modelforms=form_class,
        per_page=10,
        columns=columns,
        edition_rout=edition_rout
    )

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # email = form.cleaned_data['email']
            form.save()
            # print("formulario salvo")
            # define_setting(
            #     request=request,
            #     model_class=model,
            #     form_class=form_class,
            #     email=email
            # )
            return redirect(redirect_url)


    forms, dados_paginados = dt_and_forms.get_data_and_forms()

    url_action = reverse(redirect_url)

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
            'modal_button': modal_button
        }
    )


def edit_generic_view(request, model_class, form_class, template_name, id_random, app_name, redirect_url_name, redirect_close_button):
    objeto = get_object_or_404(model_class, id_random=id_random)
    forms = form_class(instance=objeto)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect(reverse(redirect_url_name, kwargs={'id_random': id_random}))

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
        }
    )