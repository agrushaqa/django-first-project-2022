from django import forms
from user.models import Avatar
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm


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
