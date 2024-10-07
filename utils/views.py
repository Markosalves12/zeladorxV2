from django.shortcuts import render, redirect, get_object_or_404
from utils.utils import DataTableAndForms, aplicar_filtros_dinamicos, define_filters, paginate
from django.urls import reverse
from settings.utils import define_setting
from permissionscontrol.utils import configurate_permissions
from django.contrib import messages

def generic_view(request, model, form_class, template_name, columns, edition_rout, app_name,
                 text_button_open_modal, text_button_save,  header_model,
                 redirect_url, form_search, filtro_mapeamento, sform_search=False, userid=False,
                 button_export_tittle=False, button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
                 status=['Mobilizado'],
                 link_tipos=None, modal_button=True, configurate_gerente=False, history_rout=False,
                 permission_view=True, permission_edit=False, permission_crate=False,
                 permission_accompany=False):

    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    dt_and_forms = DataTableAndForms(
        request=request,
        model=model,
        modelforms=form_class,
        per_page=15,
        columns=columns,
        edition_rout=edition_rout,
        history_rout=history_rout,
        userid=userid,
        filtro_mapeamento=filtro_mapeamento
    )

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, request=request, userid=userid)
        print(form.errors)
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

                messages.info(
                    request=request,
                    message=f'alterações salvas'
                )

                return redirect(redirect_url, request.session.get('userid', ''))

            else:
                form.save()

                messages.info(
                    request=request,
                    message=f'alterações salvas'
                )

                return redirect(redirect_url, request.session.get('userid', ''))

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    forms, dados_paginados, get_data = dt_and_forms.get_data_and_forms()

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
            'form_search': form_search,
            'sform_search': sform_search,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'button_export_tittle': button_export_tittle,
            'button_export_link': reverse(
                f'{button_export_link}',
                kwargs={
                    'userid': userid,
                    'status': ','.join(status),
                    **get_data
                }
            ),
            'link_tipos': link_tipos,
            'modal_button': modal_button,
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate,
            'permission_accompany': permission_accompany,
        }
    )

def edit_generic_view(request, model_class, form_class, template_name, id_random, app_name, redirect_url_name,
                      url_desmobilize, url_rehabilitate,
                      redirect_close_button, link_tipos=None, permission_edit=False, permission_exclude=False,
                      permission_desmobilize=False, permission_rehabilitate=False,
                      ):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    objeto = get_object_or_404(model_class, id_random=id_random)

    forms = form_class(instance=objeto, request=request, userid=request.session.get('userid', ''))

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=objeto, request=request, userid=request.session.get('userid', ''))
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'alterações salvas'
            )

            return redirect(reverse(redirect_url_name, kwargs={'userid': request.session.get('userid', ''), 'id_random':id_random}))

        messages.error(
            request=request,
            message=f'Algo de errado'
        )


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
            'link_tipos': link_tipos,
            'permission_exclude': permission_exclude,
            'permission_desmobilize': permission_desmobilize,
            'permission_rehabilitate': permission_rehabilitate,
            'url_desmobilize': url_desmobilize,
            'url_rehabilitate': url_rehabilitate,
            'objeto': objeto
        }
    )


def gerneric_alter_status(request, model_class, redirect_url_name, id_random, new_status, message):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    objeto = get_object_or_404(model_class, id_random=id_random)
    objeto.status = new_status
    objeto.save()

    if new_status == 'Mobilizado':
        messages.success(
            request=request,
            message=message
        )

    elif new_status == 'Desmobilizado':
        messages.warning(
            request=request,
            message=message
        )

    return redirect(redirect_url_name)


def generic_view_history(request, userid, id_random, app_name, objeto, objetos, type_exibition, type_export, form_search,
                         sform_search, filtro_mapeamento, export_pdf, export_excel, redirect_close_button,
                         foto_objeto=None, Foto=False):

    get_data = define_filters(request=request, isnull=True)

    if request.method == 'GET':
        get_data = request.GET.dict()
        objetos = aplicar_filtros_dinamicos(objetos, get_data, filtro_mapeamento)

        get_data = define_filters(request=request, isnull=False)

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=2
    )

    return render(
        request=request,
        template_name='history/history.html',
        context={
            'app_name': f'{app_name}',
            'objeto': objeto,
            'foto_objeto': foto_objeto,
            'Foto': Foto,
            'type_exibition': type_exibition,
            'form_search': form_search,
            'sform_search': sform_search,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'dados_paginados': dados_paginados,
            'export_pdf': reverse(
                f'{export_pdf}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'export_excel': reverse(
                viewname=f'{export_excel}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'redirect_close_button': reverse(redirect_close_button, kwargs={'userid': userid})
        }
    )