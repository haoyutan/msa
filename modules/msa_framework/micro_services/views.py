from django.http import Http404
from rest_framework.response import Response

from msa_framework.views import LoggedAPIView

from .authentication import MicroServiceSecretAuthentication
from .permissions import IsMicroService

from . import models, serializers


class MicroServiceDetails(LoggedAPIView):
    """
    Get the details of a micro service.
    """

    authentication_classes = (MicroServiceSecretAuthentication,)
    permission_classes = (IsMicroService,)
    serializer_class = serializers.MicroServiceSerializer
    model_class = models.MicroService

    def get(self, request, name=None, format=None):
        if name is None:
            name = request.user.name

        try:
            micro_service = self.model_class.objects.get(name=name)
        except models.MicroService.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(micro_service)
        return Response(serializer.safe_data(request.user))

micro_service_details = MicroServiceDetails.as_view()


class MicroServiceList(LoggedAPIView):
    """
    Get the details of all micro services.
    """

    authentication_classes = (MicroServiceSecretAuthentication,)
    permission_classes = (IsMicroService,)
    serializer_class = serializers.MicroServiceSerializer
    model_class = models.MicroService

    def get(self, request, format=None):
        micro_services = self.model_class.objects.all()
        result = {}
        for micro_service in micro_services:
            serializer = self.serializer_class(micro_service)
            data = serializer.safe_data(request.user)
            result[data['name']] = data
        return Response(result)

micro_service_list = MicroServiceList.as_view()


class MicroServiceConfigurationList(LoggedAPIView):
    """
    Get the configurations of a micro service.
    """

    authentication_classes = (MicroServiceSecretAuthentication,)
    permission_classes = (IsMicroService,)
    serializer_class = serializers.MicroServiceConfigurationSerializer
    model_class = models.MicroServiceConfiguration

    def get(self, request, ms_name=None, format=None):
        if ms_name is None:
            ms_name = request.user.name

        try:
            ms = models.MicroService.objects.get(name=ms_name)
        except models.MicroService.DoesNotExist:
            raise Http404

        configurations = self.model_class.objects.filter(micro_service=ms)
        result = {}
        for conf in configurations:
            if not conf.is_public and ms_name != request.user.name:
                continue
            result[conf.key] =  {
                'value': conf.value,
                'default': conf.default,
                'is_public': conf.is_public,
            }
        return Response(result)

micro_service_configuration_list = MicroServiceConfigurationList.as_view()
