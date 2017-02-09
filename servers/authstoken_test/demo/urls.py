from django.conf.urls import include, url
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = (
    url(r'^$', views.AuthSTokenDemo.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
