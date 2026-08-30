from rest_framework.permissions import BasePermission


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('GET', 'HEAD', 'OPTIONS') or (
            request.user.is_authenticated and request.user.is_staff
        )


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
