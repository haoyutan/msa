from django.db import models

from msa.utils import random_hex_string


class MicroService(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True)
    url = models.CharField(max_length=128, blank=False)
    is_external = models.BooleanField(default=False)
    secret = models.CharField(max_length=40, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    token_for_read = models.CharField(max_length=40, blank=False, unique=True)
    token_for_write = models.CharField(max_length=40, blank=False, unique=True)
    token_for_admin = models.CharField(max_length=40, blank=False, unique=True)
    package_source = models.CharField(max_length=64, blank=True)
    package_version = models.CharField(max_length=16, blank=True)

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = random_hex_string(40)
        if not self.token_for_read:
            self.token_for_read = random_hex_string(40)
        if not self.token_for_write:
            self.token_for_write = random_hex_string(40)
        if not self.token_for_admin:
            self.token_for_admin = random_hex_string(40)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MicroServiceConfiguration(models.Model):
    micro_service = models.ForeignKey(MicroService)
    key = models.CharField(max_length=128, blank=False, unique=True)
    value = models.CharField(max_length=65535, blank=True)
    default = models.CharField(max_length=65535, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return '{}.{}'.format(self.micro_service.name, self.key)
