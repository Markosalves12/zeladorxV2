from django import forms

class LoginForms(forms.Form):
    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    email = forms.EmailField(
        label="Email de usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@email.com.br"
            }
        )
    )

    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sua senha"
            }
        )
    )
    # Nota depois de editar a pagina de login os estilos foram buscados da cadastro