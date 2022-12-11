from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import Avatar

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')  # '__all__'


class SettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('image',)
