from django import forms
from .models import Token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):

    class Meta:
        model = Token
        fields = ('description', 'token')

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)
