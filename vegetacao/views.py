from django.shortcuts import render, redirect
from vegetacao.models import CatalogoVegetacao
from vegetacao.forms import CatalogoVegetacaoForm
from utils.views import generic_view

# Create your views here.
def vegetacao(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=CatalogoVegetacao,
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_vegetacao',
        app_name='vegetação',
        text_button_open_modal='Adicionar nova vegetação',
        text_button_save='Salvar vegetação',
        header_model='Nova vegetação',
        redirect_url='vegetacao'
    )


def editar_vegetacao(request, userid, id_random):
    objeto = CatalogoVegetacao.objects.get(id_random=id_random)
    forms = CatalogoVegetacaoForm(instance=objeto)

    if request.method == 'POST':
        form = CatalogoVegetacaoForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('editar_vegetacao', id_random)

    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Editar vegetação',
            'id_random': id_random,
            'text_button': 'Salvar'
        }
    )
