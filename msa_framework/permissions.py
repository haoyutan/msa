from rest_framework.permissions import BasePermission


class DenyAny(BasePermission):

    def has_permission(self, request, view):
        return False
