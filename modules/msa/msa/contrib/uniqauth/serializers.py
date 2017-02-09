import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .exceptions import *
from .static import *
from .models import *


# Model serializers

class JSONField(serializers.Field):
    def _loads_data(self, data):
        try:
            value = json.loads(data)
        except:
            return data
        return value

    def to_representation(self, obj):
        return self._loads_data(obj)

    def to_internal_value(self, data):
        return self._loads_data(data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=None)
    #date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = User
        #fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    #update = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    misc = JSONField()

    class Meta:
        model = Account
        #fields = '__all__'


class AccessLogSerializer(serializers.ModelSerializer):
    t = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = AccessLog
        #fields = '__all__'


class PasswordHistorySerializer(serializers.ModelSerializer):
    t = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = PasswordHistory
        #fields = '__all__'


# View serializers

def public_validate_password(value):
    v = value.lower()
    if v == EMPTY_MD5:
        raise serializers.ValidationError('This field may not be empty encryption value.')
    else:
        return v


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=32)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError(Conflict.default_detail)
        except ObjectDoesNotExist:
            return value

    def validate_password(self, value):
        return public_validate_password(value)


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=32)

    def validate_password(self, value):
        return public_validate_password(value)


class PasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password_old = serializers.CharField(max_length=32)
    password_new = serializers.CharField(max_length=32)

    def validate_password_old(self, value):
        return public_validate_password(value)

    def validate_password_new(self, value):
        return public_validate_password(value)

    def validate(self, data):
        if data['password_old'] == data['password_new']:
            raise serializers.ValidationError('The new password must be different from the old password.')
        else:
            return data


class MiscSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=128)
    value = JSONField()


class AdminResetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=32)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError(NotFound.default_detail)

    def validate_password(self, value):
        return public_validate_password(value)
