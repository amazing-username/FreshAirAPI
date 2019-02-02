from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    pass

class Status(models.Model):
    message = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('api.User', related_name='statuses', on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
