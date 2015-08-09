from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from msa.views import LoggedAPIView


class DummyAPI(LoggedAPIView):
    """
    A dummy API for testing.
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, name=None, format=None):
        return Response({'method': 'GET', 'request.data': request.data})

    def post(self, request, name=None, format=None):
        return Response({'method': 'POST', 'request.data': request.data})

    def put(self, request, name=None, format=None):
        return Response({'method': 'PUT', 'request.data': request.data})

    def delete(self, request, name=None, format=None):
        return Response({'method': 'DELETE', 'request.data': request.data})

dummy_api = DummyAPI.as_view()
