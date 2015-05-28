from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from msa_framework.views import LoggedAPIView


class MasterServerInfo(LoggedAPIView):
    """
    Show master server information.
    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({'master_sever_name': settings.MSA_MASTER_SERVER_NAME})

master_server_info = MasterServerInfo.as_view()
