from django import forms
from catalogo_de_materiais.models import CatalogoMaterial, CategoriaMaterial, ConsumoMateriais

class MaterialForms(forms.ModelForm):
    class Meta:
        model = CatalogoMaterial
        fields = ['nome', 'CategoriaDoMaterial', 'FormaDeConsumo', 'EmpresaSecundaria']

        labels = {
            'nome': 'Nome do material',
            'CategoriaDoMaterial': 'Categoria do material',
            'FormaDeConsumo': 'Forma de consumo',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'CategoriaDoMaterial': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'FormaDeConsumo': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaSecundaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class CategoriaMaterialForms(forms.ModelForm):
    class Meta:
        model = CategoriaMaterial
        fields = ['nome', 'EmpresaSecundaria']

        labels = {
            'nome': 'Categoria do material',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaSecundaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class ConsumoMaterialForms(forms.ModelForm):
    class Meta:
        model = ConsumoMateriais
        fields = ['nome', 'EmpresaSecundaria']

        labels = {
            'nome': 'Forma de consumo',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'EmpresaSecundaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }