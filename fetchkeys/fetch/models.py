from django.db import models
from django.conf import settings


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens')
    description = models.CharField(max_length=100)
    token = models.CharField(max_length=40, unique=True)


class UserRepository(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repos')
    name = models.CharField(max_length=200)


class DeployKey(models.Model):
    repository = models.ForeignKey('UserRepository', related_name='keys')
    title = models.CharField(max_length=100)
    key = models.TextField()
