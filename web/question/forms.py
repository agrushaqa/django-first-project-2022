from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Avatar, CreateQuestion, Tag, User


class ListQuestionsForm(forms.ModelForm):
    class Meta:
        model = CreateQuestion
        fields = '__all__'


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = CreateQuestion
        fields = ('description',)


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = CreateQuestion
        fields = ('title', 'description')


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')  # '__all__'


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)

    def clean_tag(self):
        data = self.cleaned_data['tag'].split(',')[:3]
        return data

    def save(self):
        data = self.cleaned_data
        list_result = []
        for i_data in data['tag']:
            current_tag = Tag(tag=i_data)
            current_tag.save()
            list_result.append(current_tag)
        return list_result


class SettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('image',)
