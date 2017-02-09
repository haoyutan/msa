from django.contrib.auth import authenticate
from msa.utils.ipware import get_ip
from msa.views import LoggedAPIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import *


class Register(LoggedAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        pp = self.serializer_class(data=request.data)
        if pp.is_valid():
            username = pp.validated_data['username']
            password = pp.validated_data['password']
            if Account.objects.count() <= 0:
                user = User.objects.create_superuser(username=username, password=password, email=None)
            else:
                user = User.objects.create_user(username=username, password=password, email=None)
            account = Account(user=user)
            #account.save()
            password_history = PasswordHistory(account=account, ip=get_ip(request), password=password)
            password_history.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise BadRequest(pp.errors)


class LogIn(LoggedAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = LogInSerializer

    def get(self, request):
        pp = self.serializer_class(data=request.GET)
        if pp.is_valid():
            username = pp.validated_data['username']
            password = pp.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                '''
                if not created:
                    token.created = timezone.now()
                    token.save()
                '''
                account = Account.objects.get(user=user)
                access_log = AccessLog(account=account, ip=get_ip(request), token=token)
                access_log.save()
                return Response({'token': token.key})
            else:
                raise Unauthorized()
        else:
            raise BadRequest(pp.errors)


class Verify(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class Password(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordSerializer

    def post(self, request):
        pp = self.serializer_class(data=request.data)
        if pp.is_valid():
            username = pp.validated_data['username']
            password_old = pp.validated_data['password_old']
            password_new = pp.validated_data['password_new']
            user = authenticate(username=username, password=password_old)
            if user is not None:
                user.set_password(password_new)
                user.save()
                account = Account.objects.get(user=user)
                #account.update = timezone.now()
                account.save()
                password_history = PasswordHistory(account=account, ip=get_ip(request), password=password_new)
                password_history.save()
                user.auth_token.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                raise Unauthorized()
        else:
            raise BadRequest(pp.errors)


class Detail(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request):
        return Response(self.serializer_class(Account.objects.get(user=request.user)).data)


class Misc(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MiscSerializer

    def post(self, request):
        pp = self.serializer_class(data=request.data)
        if pp.is_valid():
            account = Account.objects.get(user=request.user)
            if account.misc:
                misc = json.loads(account.misc)
            else:
                misc = dict()
            
            misc[pp.validated_data['field']] = pp.validated_data['value']
            account.misc = json.dumps(misc)
            account.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise BadRequest(pp.errors)


class AdminList(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class = AccountSerializer

    def get(self, request):
        return Response(self.serializer_class(Account.objects.all(), many=True).data)


class AdminReset(LoggedAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class = AdminResetSerializer

    def put(self, request):
        pp = self.serializer_class(data=request.data)
        if pp.is_valid():
            username = pp.validated_data['username']
            password = pp.validated_data['password']
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            account = Account.objects.get(user=user)
            #account.update = timezone.now()
            account.save()
            password_history = PasswordHistory(account=account, ip=get_ip(request), password=password)
            password_history.save()
            user.auth_token.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            raise BadRequest(pp.errors)
