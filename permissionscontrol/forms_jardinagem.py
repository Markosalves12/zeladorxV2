from django import forms
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem
from empresasecundario.utils import define_empresas

class PermissionsAccessJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(PermissionsAccessJardinagemForms, self).__init__(*args, **kwargs)
        if userid:
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']
            empresas_secundarias_ids = empresas['empresas_secundarias_ids']

            self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
            )

    Permissions = forms.ModelMultipleChoiceField(
        queryset=PermissionsJardinagem.objects.all().order_by('Permissions'),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Permissões concedidas',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = PermissionsAccessJardinagem

        fields = ['Gerente', 'Permissions']

        labels = {
            'Gerente': 'Gerente',
            'Permissions': 'Permissões concedidas',
        }

        widgets = {
            'Gerente': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
