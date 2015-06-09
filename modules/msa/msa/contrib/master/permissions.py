from rest_framework.permissions import BasePermission

from .models import MicroService


class IsMicroService(BasePermission):
    def has_permission(self, request, view):
        return type(request.user) is MicroService
