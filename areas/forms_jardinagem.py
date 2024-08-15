from django import forms
from areas.models_jardinagem import AreasJardins

class AreasJardinsForms(forms.ModelForm):
    class Meta:
        model = AreasJardins
        fields = ['nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto']

        labels = {
            'nome': 'Nome da região',
            'dimensao': 'Dimensão da área em M²',
            'vegetacao': 'Vegetação predominante',
            'Terreno': 'Terreno predominante',
            'servico': 'Serviço principal aplicado',
            'localidade': 'Localidade',
            'foto': 'Foto da região',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'dimensao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'Terreno': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'vegetacao': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'localidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }



