from rest_framework.permissions import BasePermission

from .models import SUser



class IsSTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, SUser)
