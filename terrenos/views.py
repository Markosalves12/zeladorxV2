from django.shortcuts import render, redirect
from terrenos.models import Terreno
from terrenos.forms import TerrenoForms
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions

# Create your views here.
def terrenos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['260: Pode visualizar terrenos']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['259: Pode editar terrenos']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['258: Pode criar novos terrenos']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=Terreno,
        form_class=TerrenoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_terreno',
        app_name='Terrenos',
        text_button_open_modal='Adicionar novo terreno',
        text_button_save='Salvar terreno',
        header_model='Novo terreno',
        redirect_url='terrenos',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate
    )


def editar_terreno(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['259: Pode editar terrenos']
    )

    objeto = Terreno.objects.get(id_random=id_random)
    forms = TerrenoForms(instance=objeto)

    if request.method == 'POST':
        form = TerrenoForms(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('editar_terreno', id_random)

    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Editar terreno',
            'id_random': id_random,
            'text_button': 'Salvar',
            'permission_edit': permission_edit
        }
    )