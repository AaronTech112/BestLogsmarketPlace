from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 'email', 'phone_number','password1', 'password2'
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'first_name', 'last_name', 'email', 'phone_number', ]