from django import forms
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from empresasecundario.utils import define_empresa_primaria_ids

class CatalogoServicoLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid, **kwargs):
        super(CatalogoServicoLimpezaPredialForms, self).__init__(*args, **kwargs)
        if userid:
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)

            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids
            )

    class Meta:
        model = CatalogodeServicoLimpezaPredial
        fields = ['nome', 'EmpresaSecundaria', ]

        labels = {
            'nome': 'Nome do serviço',
            'EmpresaSecundaria': 'Empresa prestadora',
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
