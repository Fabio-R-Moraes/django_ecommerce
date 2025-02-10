from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        error_messages={"required": "Obrigatório o preenchimento do nome"},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite o seu nome completo",
            }
        )
    )
    email = forms.EmailField(
        error_messages={"invalid": "Digite um e-mail válido"},
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu e-mail",
            }
        )
    )
    content = forms.CharField(
        error_messages={"required": "É obrigatório digitar algum recado"},
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Seu texto aqui..."
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not "gmail.com" in email:
            raise forms.ValidationError("Só aceitamos e-mails com <gmail.com>...")
        
        return email
    
    #def clean_content(self):
    #    raise forms.ValidationError("O conteúdo está errado...")