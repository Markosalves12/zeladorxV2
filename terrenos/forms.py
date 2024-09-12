from terrenos.models import Terreno
from django import forms
from empresasecundario.utils import define_empresa_primaria_ids

class TerrenoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(TerrenoForms, self).__init__(*args, **kwargs)
        if userid:
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)
            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids
            )

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

