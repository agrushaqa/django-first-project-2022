from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import CreateAnswer, CreateQuestion


class QuestionListSerializer(ModelSerializer):
    class Meta:
        model = CreateQuestion
        fields = '__all__'


class ListAnswersSerializer(ModelSerializer):
    class Meta:
        model = CreateAnswer
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
