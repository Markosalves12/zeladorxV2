from empresasecundario.models import EmpresaSecundaria
from django import forms
from empresasecundario.utils import define_empresas

class EmpresaSecundariaJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(EmpresaSecundariaJardinagemForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']

            # Ajustar o queryset do campo 'empresaprimaria'
            self.fields['empresaprimaria'].queryset = self.fields['empresaprimaria'].queryset.filter(
                id_random__in=empresas_primarias_ids
            )

            self.fields['setor'].choices = [('Jardinagem', 'Jardinagem')]

    class Meta:
        model = EmpresaSecundaria
        fields = ['nome', 'razao_social', 'CNPJ', 'logo', 'setor', 'empresaprimaria', ]
        labels = {
            'nome': 'Nome',
            'razao_social': 'Razão social',
            'CNPJ': 'CNPJ (apenas os números)',
            'setor': 'Setor',
            'empresaprimaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'razao_social': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'CNPJ': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'logo': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'setor': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'empresaprimaria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }