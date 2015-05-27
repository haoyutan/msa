from django.http import Http404
from rest_framework.response import Response

from msa_framework.views import LoggedAPIView

from .authentication import MicroServiceSecretAuthentication
from .permissions import IsMicroService
from .models import MicroService
from .serializers import MicroServiceSerializer


class MicroServiceDetails(LoggedAPIView):
    """
    Get the details of a micro service.
    """

    authentication_classes = (MicroServiceSecretAuthentication,)
    permission_classes = (IsMicroService,)
    serializer_class = MicroServiceSerializer

    def get(self, request, name=None, format=None):
        if name is None:
            name = request.user.name

        try:
            micro_service = MicroService.objects.get(name=name)
        except MicroService.DoesNotExist:
            raise Http404

        serializer = MicroServiceSerializer(micro_service)
        return Response(serializer.safe_data(request.user))

micro_service_details = MicroServiceDetails.as_view()


class MicroServiceList(LoggedAPIView):
    """
    Get the details of all micro services.
    """

    authentication_classes = (MicroServiceSecretAuthentication,)
    permission_classes = (IsMicroService,)
    serializer_class = MicroServiceSerializer

    def get(self, request, format=None):
        micro_services = MicroService.objects.all()
        result = []
        for micro_service in micro_services:
            serializer = MicroServiceSerializer(micro_service)
            result.append(serializer.safe_data(request.user))
        return Response(result)

micro_service_list = MicroServiceList.as_view()
