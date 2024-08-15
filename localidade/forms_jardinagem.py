from django import forms
from localidade.models_Jardinagem import LocalidadeJardiangem


class LocalidadeJardinagemForms(forms.ModelForm):
    class Meta:
        model = LocalidadeJardiangem
        fields = ['nome', 'lat_med', 'long_med', 'unidade', ]
        labels = {
            'nome': 'Localidade',
            'lat_med': 'Latitude média',
            'long_med': 'Longitude média',
            'unidade': 'Unidade'
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lat_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'long_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }