from django.conf.urls import include, url
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

from msa.views import StaticView
from . import views


urlpatterns = (
    url(r'^$', views.micro_service_list),
    url(r'^micro-services/$', views.micro_service_list),
    url(r'^micro-service/$', views.micro_service_details),
    url(r'^micro-service/(?P<name>[-\w]+)/$', views.micro_service_details),
    url(r'^configuration/$', views.micro_service_configuration_list),
    url(r'^configuration/(?P<ms_name>[-\w]+)/$',
        views.micro_service_configuration_list),
)

urlpatterns = format_suffix_patterns(urlpatterns)


def make_master_top_urlpatterns(msa_master_name):
    top_url_patterns = (
        url(r'^$',
            StaticView.as_view(content = {'msa_master_name': msa_master_name})),
        url(r'^{}/'.format(msa_master_name),
            include('msa.contrib.master.urls')),
    )
    return top_url_patterns
