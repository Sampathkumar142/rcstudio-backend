from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    first_name = None
    last_name = None
    phoneNumber = models.BigIntegerField(null=True)


class pcloudAccount(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    auth = models.CharField(max_length=200, unique=True)
    lastUpdate = models.DateField(auto_now=True)
