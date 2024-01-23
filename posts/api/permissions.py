from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser
from rest_framework.request import Request


class IsOwnerOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_staff
            or request.user == obj.autor
        )
