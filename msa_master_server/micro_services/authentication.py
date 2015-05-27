from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header, BaseAuthentication,
)

from .models import MicroService


class MicroServiceSecretAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.authenticate_header(request):
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, secret):
        try:
            micro_service = MicroService.objects.get(secret=secret)
        except MicroService.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid secret.')

        return (micro_service, secret)

    def authenticate_header(self, request):
        # MSS stands for 'Micro Service Secret'
        return b'mss'
