from django.conf.urls import url

from .views import *


urlpatterns = [
    # ------- Single User Management -------
    url(r'register/$', Register.as_view()),
    url(r'login/$', LogIn.as_view()),
    url(r'verify/$', Verify.as_view()),
    url(r'password/$', Password.as_view()),
    url(r'detail/$', Detail.as_view()),
    url(r'misc/$', Misc.as_view()),
    # ------- Multiple User Management (Admin Only) -------
    url(r'admin/list/$', AdminList.as_view()),
    url(r'admin/reset/$', AdminReset.as_view()),
]
