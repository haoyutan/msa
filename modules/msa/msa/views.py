import logging, json, datetime
from uuid import uuid1
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .utils import get_ip, JSONEncoder



class LoggedAPIView(APIView):
    api_logger = logging.getLogger('API')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_id = str(uuid1())


    def initialize_request(self, request, *args, **kwargs):
        self._log_raw_request(request)
        return super().initialize_request(request, *args, **kwargs)


    def initial(self, request, *args, **kwargs):
        self._log_request(request)
        super().initial(request, *args, **kwargs)
        self._log_authentication(request)


    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self._log_response(response)
        return response


    def _log_raw_request(self, request):
        msg = '{}|{}|{}'.format(self._log_id, 'RAW_REQUEST',
                                self._extract_raw_request_info(request))
        self.api_logger.info(msg)


    def _log_request(self, request):
        info = {
            'method'        : request.method.upper(),
            'uri'           : request.build_absolute_uri(),
            'content_type'  : request.content_type,
            'authorization' : request.META.get('HTTP_AUTHORIZATION'),
            'data'          : str(request.data),
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'REQUEST', info_str)
        self.api_logger.info(msg)


    def _log_authentication(self, request):
        info = {
            'user_type'     : type(request.user).__name__,
            'id'            : request.user.id,
            'detail'        : str(request.user),
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'AUTH', info_str)
        self.api_logger.info(msg)


    def _log_response(self, response):
        info = {
            'status'        : (response.status_code, response.status_text),
            'content'       : response.data,
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'RESPONSE', info_str)
        self.api_logger.info(msg)


    def _extract_raw_request_info(self, request):
        info = {
            'method'       : request.method,
            'uri'          : request.build_absolute_uri(),
            'content_type' : request.META.get('CONTENT_TYPE', ''),
            'remote_addr'  : get_ip(request),
        }
        return info


    def json_dump(self, data):
        return json.dumps(data, sort_keys=True, cls=JSONEncoder)



class StaticView(LoggedAPIView):
    permission_classes = (AllowAny,)
    content = {'message': 'Hello, MSA.'}

    def get(self, request, format=None):
        return Response(self.content)
