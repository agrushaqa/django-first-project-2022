from betterforms.multiform import MultiModelForm
from common.models import CreateQuestion, Tag
from django import forms
from django.forms import ModelForm


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


class AskMeMultiForm(MultiModelForm):
    form_classes = {
            'ask_form': AskQuestionForm,
            'tag_form': TagForm,
        }
