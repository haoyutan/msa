from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


msa_urlpatterns_default = []

msa_allow_admin_site = getattr(settings, 'MSA_ALLOW_ADMIN_SITE', False)
if msa_allow_admin_site:
    msa_urlpatterns_default.append(url(r'^admin/', include(admin.site.urls)))
