from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class InternalError(APIException):
    status_code = 500
    default_detail = _('Internal error.')
