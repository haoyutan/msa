import os

from django.conf.urls import include, url

from msa.urls import msa_default_urlpatterns



urlpatterns = msa_default_urlpatterns + [
    url(r'^auth/', include('msa.contrib.uniqauth.urls')),
]
