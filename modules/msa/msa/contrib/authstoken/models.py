import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _



@python_2_unicode_compatible
class SUser(models.Model):
    sid = models.CharField(_("sid"), max_length=20, primary_key=True)
    description = models.CharField(_("name"), max_length=128, blank=True)
    is_active = models.BooleanField(null=False, default=0)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)


    class Meta:
        verbose_name = _("SUser")
        verbose_name_plural = _("SUsers")


    @property
    def id(self):
        return '${}'.format(self.sid)


    def __str__(self):
        return self.sid



@python_2_unicode_compatible
class SToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    suser = models.ForeignKey(
                SUser, related_name='auth_stoken',
                on_delete=models.CASCADE, verbose_name=_("SUser")
            )
    host = models.CharField(_("Host"), max_length=128, null=False,
                            blank=True, default='*')
    created = models.DateTimeField(_("Created"), auto_now_add=True)


    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'msa.contrib.authstoken' not in settings.INSTALLED_APPS
        verbose_name = _("SToken")
        verbose_name_plural = _("STokens")


    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SToken, self).save(*args, **kwargs)


    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()


    def __str__(self):
        return self.key
