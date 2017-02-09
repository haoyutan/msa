from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from msa.views import LoggedAPIView
from msa.contrib.authstoken.authentication import STokenAuthentication
from msa.contrib.authstoken.permissions import IsSTokenAuthenticated



class AuthSTokenDemo(LoggedAPIView):
    authentication_classes = (STokenAuthentication,)
    permission_classes = (IsSTokenAuthenticated,)


    def _process(self, request, name=None, format=None):
        return Response({'method': 'GET', 'request.data': request.data,
                         'request.user': request.user.id})


    def get(self, request, name=None, format=None):
        return self._process(request)


    def post(self, request, name=None, format=None):
        return self._process(request)


    def put(self, request, name=None, format=None):
        return self._process(request)


    def delete(self, request, name=None, format=None):
        return self._process(request)


    def get_view_name(self):
        return 'SToken Authorization Demo'
