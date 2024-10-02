from django import forms
from gerente.models import Gerente
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas

class GerenteLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(GerenteLimpezaPredialForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                setor__setor='Limpeza predial',
                status__in=['Mobilizado']
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
                empresaprimaria__id_random__in=empresas_primarias_ids,
                setor__setor='Limpeza predial',
            )

            self.fields['empresasecundaria'] = forms.ModelMultipleChoiceField(
                queryset=EmpresaSecundaria.objects.all(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': 'max-height: 40px; overflow-y: auto;'
                    }
                ),
                label='Empresas que atende',
                required=False,
                initial=None
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
            'superuser': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }