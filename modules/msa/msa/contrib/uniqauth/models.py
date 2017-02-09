from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account',
                                on_delete=models.CASCADE,
                                verbose_name='User')
    update = models.DateTimeField('Updated', auto_now=True)
    misc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class AccessLog(models.Model):
    account = models.ForeignKey(Account)
    t = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    token = models.CharField(max_length=40)


class PasswordHistory(models.Model):
    class Meta:
        verbose_name = 'Password history'
        verbose_name_plural = 'Password histories'

    account = models.ForeignKey(Account)
    t = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    password = models.CharField(max_length=32)
