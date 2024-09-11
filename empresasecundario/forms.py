from empresasecundario.models import EmpresaSecundaria
from django import forms
from gerente.models import Gerente
from empresasecundario.utils import define_empresa_primaria_ids

class EmpresaSecundariaForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(EmpresaSecundariaForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if userid:
            gerente = Gerente.objects.get(id_random=userid)
            empresas_primarias_ids = define_empresa_primaria_ids(request=request, userid=userid)

            # Ajustar o queryset do campo 'empresaprimaria'
            self.fields['empresaprimaria'].queryset = self.fields['empresaprimaria'].queryset.filter(
                id_random__in=empresas_primarias_ids
            )

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