import os

from django.conf import settings
from django.conf.urls import include, url

from msa.urls import msa_default_urlpatterns


msa_dummy_name = getattr(settings, 'MSA_DUMMY_NAME')
if not msa_dummy_name:
    msa_dummy_name = 'change-my-name'

urlpatterns = msa_default_urlpatterns + [
    url(r'^dummy/{}/'.format(msa_dummy_name),
        include('msa.contrib.dummy.urls')),
]
