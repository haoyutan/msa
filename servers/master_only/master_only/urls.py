import os

from django.conf.urls import include, url
from django.contrib import admin

from msa.views import MessageView


MASTER_NAME = os.environ.get('MASTER_NAME', 'sir')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MessageView.as_view(message = MASTER_NAME)),
    url(r'^{}/'.format(MASTER_NAME), include('msa.contrib.master.urls')),
]
