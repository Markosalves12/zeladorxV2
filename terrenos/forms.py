from terrenos.models import Terreno
from django import forms
from empresasecundario.utils import define_empresas

class TerrenoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(TerrenoForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                empresaprimaria__status__in=['Mobilizado'],
                id_random__in=empresas_secundarias_ids,
                status__in=['Mobilizado']
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

    class Meta:
        model = Terreno
        fields = ['nome', 'EmpresaSecundaria', ]
        labels = {
            'nome': 'Nome do terreno',
            'EmpresaSecundaria': 'Empresa operadora'
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
            )
        }

