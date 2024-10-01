from django import forms
from gerente.models import Gerente
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas

class GerenteJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(GerenteJardinagemForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                setor__setor='Jardinagem',
                status__in=['Mobilizado']
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

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
        fields = ['username', 'email', 'empresasecundaria', 'superuser', ]
        labels = {
            'username': 'Nome do gerente',
            'email': 'Email de contato',
            'empresasecundaria': 'Empresa Secundaria',
            'superuser': 'É super usuário'
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
            'superuser': forms.CheckboxInput(
                attrs={
                    'class': 'checkbox'
                }
            ),
        }