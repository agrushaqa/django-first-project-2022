from django.db import models
from user.models import User


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=256, null=True, blank=True,
                           default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CreateQuestion(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
