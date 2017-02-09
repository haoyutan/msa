from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from msa.utils.ipware import get_ip

from .models import SToken



class STokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "SToken ".  For example:
        Authorization: SToken 401f7ac837da42b97f613d789819ff93537bee6a
    """


    keyword = 'SToken'
    model = SToken


    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)


    def authenticate_credentials(self, key, request):
        model = self.model
        try:
            stoken = model.objects.select_related('suser').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid stoken.'))

        if not self._check_host_pattern(get_ip(request), stoken.host):
            raise AuthenticationFailed(_('Unauthorized ip address.'))

        if not stoken.suser.is_active:
            raise AuthenticationFailed(_('SUser inactive or deleted.'))

        return (stoken.suser, stoken)


    def authenticate_header(self, request):
        return self.keyword


    def _check_host_pattern(self, ip_addr, pattern):
        # NOTE: This is a quick and dirty implementation.
        # TODO: Improve it asap.
        if pattern == '*':
            return True
        elif ip_addr == pattern:
            return True

        return False
