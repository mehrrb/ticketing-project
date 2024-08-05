from rest_framework.permissions import BasePermission
from .models import Ticket



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if obj.user.email == request.user.email:
                    return True
            return False
        except:
            return False
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user and request.is_superuser:
                return True
            return False
        except:
            return False
            