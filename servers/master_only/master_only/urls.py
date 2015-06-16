import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from msa.views import StaticView
from msa.urls import msa_default_urlpatterns


msa_master_name = getattr(settings, 'MSA_MASTER_NAME')
if not msa_master_name:
    msa_master_name = 'change-my-name'

urlpatterns = msa_default_urlpatterns + [
    url(r'^$',
        StaticView.as_view(content = {'msa_master_name': msa_master_name})),
    url(r'^{}/'.format(msa_master_name), include('msa.contrib.master.urls')),
]
