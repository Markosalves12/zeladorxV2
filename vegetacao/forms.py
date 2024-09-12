from django import forms
from vegetacao.models import CatalogoVegetacao
from empresasecundario.utils import define_empresas

class CatalogoVegetacaoForm(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(CatalogoVegetacaoForm, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                id_random__in=empresas_secundarias_ids
            )
    class Meta:
        model = CatalogoVegetacao
        fields = ['nome', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Vegetação',
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