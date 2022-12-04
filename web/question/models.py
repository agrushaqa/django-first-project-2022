from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=256, null=True, blank=True,
                           default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    pass


class Avatar(models.Model):
    image = models.FileField(upload_to='avatars', null=True, blank=True,
                             default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CreateQuestion(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CreateAnswer(models.Model):
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(CreateQuestion, on_delete=models.CASCADE)


class QuestionVote(models.Model):
    class QuestionVoteType(models.IntegerChoices):
        INDIFFERENCE = 0, 'indiffence'
        CONDEMN = 1, 'condemn'
        APPROVE = 2, 'approve'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(CreateQuestion, on_delete=models.CASCADE)
    type_id = models.PositiveSmallIntegerField(
        choices=QuestionVoteType.choices,
        default=QuestionVoteType.INDIFFERENCE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AnswerVote(models.Model):
    class AnswerVoteType(models.IntegerChoices):
        INDIFFERENCE = 0, 'indiffence'
        CONDEMN = 1, 'condemn'
        APPROVE = 2, 'approve'
        RIGHT = 3, 'right'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(CreateAnswer, on_delete=models.CASCADE)
    type_id = models.PositiveSmallIntegerField(
        choices=AnswerVoteType.choices, default=AnswerVoteType.INDIFFERENCE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
