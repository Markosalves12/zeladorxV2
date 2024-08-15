from django.shortcuts import render, redirect
from catalogo_de_materiais.models import CatalogoMaterial, CategoriaMaterial, ConsumoMateriais
from catalogo_de_materiais.forms import MaterialForms, CategoriaMaterialForms, ConsumoMaterialForms
from utils.utils import paginate

# Create your views here.
def materiais(request):
    dados = CatalogoMaterial.objects.all()
    forms = MaterialForms()

    if request.method == 'POST':
        form = MaterialForms(request.POST)
        if form.is_valid():
            #mensagem de sucesso
            form.save()
            return redirect('materiais')

    dados_paginados = paginate(
        request=request,
        data_objects=dados,
        per_page=2
    )

        #mensagem de erro
    return render(
        request=request,
        template_name='materiais/materiais.html',
        context={
            'dados_paginados': dados_paginados,
            'forms': forms,
            'app_name': 'Catálogo de materiais'
        }
    )

def categoria_material(request):
    dados = CategoriaMaterial.objects.all()
    forms = CategoriaMaterialForms()

    if request.method == 'POST':
        form = CategoriaMaterialForms(request.POST)
        if form.is_valid():
            #mensagem de sucesso
            form.save()
            return redirect('categoria_material')

    dados_paginados = paginate(
        request=request,
        data_objects=dados,
        per_page=2
    )

    #mensagem de erro
    return render(
        request=request,
        template_name='materiais/categoria_material.html',
        context={
            'dados_paginados': dados_paginados,
            'forms': forms,
        }
    )

def consumo_material(request):
    dados = ConsumoMateriais.objects.all()
    forms = ConsumoMaterialForms()

    if request.method == 'POST':
        form = ConsumoMaterialForms(request.POST)
        if form.is_valid():
            #mensagem de sucesso
            form.save()
            return redirect('consumo_material')

    dados_paginados = paginate(
        request=request,
        data_objects=dados,
        per_page=2
    )

    #mensagem de erro
    return render(
        request=request,
        template_name='materiais/consumo_material.html',
        context={
            'dados_paginados': dados_paginados,
            'forms': forms,
        }
    )