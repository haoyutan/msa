"""msa_master_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


home_urlpatterns = [
    url(r'^$', views.master_server_info),
]

home_urlpatterns = format_suffix_patterns(home_urlpatterns)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^{}/'.format(settings.MSA_MASTER_SERVER_NAME),
        include('micro_services.urls')),
]

urlpatterns = urlpatterns + home_urlpatterns
