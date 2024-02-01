from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(help_text=password_validation.password_validators_help_text_html(),
                                widget=forms.PasswordInput(attrs={"class": "form-control"}), )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), )

    class Meta:
        model = User
        fields = ("username", 'email', 'password1', 'password2')
