import logging, json
from uuid import uuid1
from rest_framework.views import APIView


class LoggedAPIView(APIView):
    logger = logging.getLogger('API')

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self._log_id = str(uuid1())

    def initial(self, request, *args, **kwargs):
        self._log_request(request)
        super().initial(request, *args, **kwargs)
        self._log_authentication(request)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self._log_response(response)
        return response

    def _log_request(self, request):
        info = {
            'method'        : request.method.upper(),
            'uri'           : request.build_absolute_uri(),
            'remote_host'   : request.META.get('REMOTE_HOST'),
            'authorization' : request.META.get('HTTP_AUTHORIZATION'),
            'POST'          : str(request.POST.dict()),
        }
        info_str = json.dumps(info, sort_keys = True)
        msg = '{}|{}|{}'.format(self._log_id, 'REQUEST', info_str)
        self.logger.info(msg)

    def _log_authentication(self, request):
        info = {
            'user_type'     : type(request.user).__name__,
            'id'            : request.user.id,
            'detail'        : str(request.user),
        }
        info_str = json.dumps(info, sort_keys = True)
        msg = '{}|{}|{}'.format(self._log_id, 'AUTH', info_str)
        self.logger.info(msg)

    def _log_response(self, response):
        info = {
            'status'        : (response.status_code, response.status_text),
            'content'       : response.data,
        }
        info_str = json.dumps(info, sort_keys = True)
        msg = '{}|{}|{}'.format(self._log_id, 'RESPONSE', info_str)
        self.logger.info(msg)
