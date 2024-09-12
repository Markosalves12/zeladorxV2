from django import forms
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem

class PermissionsAccessJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, **kwargs):
        super(PermissionsAccessJardinagemForms, self).__init__(*args, **kwargs)
        self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            id_random=userid
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
