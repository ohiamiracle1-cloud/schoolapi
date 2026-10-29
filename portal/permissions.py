from rest_framework.permissions import BasePermission
from accounts.models import User


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
        (request.user.role == User.Role.ADMIN or request.user.is_superuser))

class IsTeacherUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
        and request.user.role == User.Role.TEACHER)

class IsStudentUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
        and request.user.role == User.Role.STUDENT)