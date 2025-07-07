from django import forms
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem
from empresasecundario.utils import define_empresas

class PermissionsAccessJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(PermissionsAccessJardinagemForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid:
            self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
            ).distinct()

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
                empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                empresasecundaria__id_random__in=empresas_secundarias_ids,
                empresasecundaria__setor__setor='Jardinagem'
            ).distinct()

            # Alterando o widget dos campos de seleção múltipla para SelectMultiple
            self.fields['Permissions'] = forms.ModelMultipleChoiceField(
                queryset=PermissionsJardinagem.objects.distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': 'max-height: 40px; overflow-y: auto;'
                    }
                ),
                label='Permissões concedidas',
                required=False,
            )

    Permissions = forms.ModelMultipleChoiceField(
        queryset=PermissionsJardinagem.objects.distinct().order_by('Permissions'),
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
