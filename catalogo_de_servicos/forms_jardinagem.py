from django import forms
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from empresasecundario.utils import define_empresas

class CatalogoServicoJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid, type = 'creat/edit', **kwargs):
        super(CatalogoServicoJardinagemForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                id_random__in=empresas_secundarias_ids,
                setor__setor__in = ['Jardinagem'],
                status__in=['Mobilizado']
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                id_random__in=empresas_secundarias_ids,
            )

    class Meta:
        model = CatalogodeServicoJardinagem
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