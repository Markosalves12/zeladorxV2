from django import forms
from gerente.models import Gerente
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas

class GerenteLimpezaPredialForms(forms.ModelForm):
    def __inti__(self, *args, request, userid=str, **kwargs):
        super(GerenteLimpezaPredialForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                setor__setor='Limpeza predial',
                status__in=['Mobilizado']
            )

    empresasecundaria = forms.ModelMultipleChoiceField(
        queryset=EmpresaSecundaria.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Empresas que atende',
        required=True  # Defina como True se a seleção de colaboradores for obrigató
    )

    class Meta:
        model = Gerente
        fields = ['username', 'email', 'funcao', 'empresasecundaria']
        labels = {
            'username': 'Nome do gerente',
            'email': 'Email de contato',
            'funcao': 'Função principal',
            'empresasecundaria': 'Empresa Secundaria'
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'funcao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }