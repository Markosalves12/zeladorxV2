from django import forms
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem

class PermissionsAccessJardinagemForms(forms.ModelForm):
    Permissions = forms.ModelMultipleChoiceField(
        queryset=PermissionsJardinagem.objects.all(),
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
