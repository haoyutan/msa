import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from msa.urls import msa_urlpatterns_default
from msa.contrib.master.urls import make_master_top_urlpatterns


msa_master_name = getattr(settings, 'MSA_MASTER_NAME')
if not msa_master_name:
    msa_master_name = 'change-my-name'

urlpatterns = msa_urlpatterns_default + \
    list(make_master_top_urlpatterns(msa_master_name))
