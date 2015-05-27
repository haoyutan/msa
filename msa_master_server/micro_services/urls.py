from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = (
    url(r'^$', views.micro_service_details),
    url(r'^micro-services/$', views.micro_service_list),
    url(r'^micro-service/$', views.micro_service_details),
    url(r'^micro-service/(?P<name>[-\w]+)/$', views.micro_service_details),
)

urlpatterns = format_suffix_patterns(urlpatterns)
