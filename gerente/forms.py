from django import forms
from gerente.models import Gerente
from empresasecundario.models import EmpresaSecundaria

class GerenteForms(forms.ModelForm):
    EmpresaSecundaria = forms.ModelMultipleChoiceField(
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
        fields = ['username', 'email', 'funcao', 'EmpresaSecundaria']
        labels = {
            'username': 'Nome do gerente',
            'email': 'Email de contato',
            'funcao': 'Função principal',
            'EmpresaSecundaria': 'EmpresaSecundaria'
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