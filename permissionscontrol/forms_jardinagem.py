from django import forms
from permissionscontrol.models import PermissionsAccessJardinagem, PermissionsJardinagem

class PermissionsAccessJardinagemForms(forms.ModelForm):
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

    def __init__(self, *args, userid, **kwargs):
        super(PermissionsAccessJardinagemForms, self).__init__(*args, **kwargs)
        self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            id_random=userid
        )
        self.fields['Gerente'].required = True

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
