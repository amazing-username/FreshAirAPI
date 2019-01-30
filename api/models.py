from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Status(models.Model):
    message = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
