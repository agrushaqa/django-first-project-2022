from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Avatar(models.Model):
    image = models.FileField(upload_to='avatars', null=True, blank=True,
                             default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
