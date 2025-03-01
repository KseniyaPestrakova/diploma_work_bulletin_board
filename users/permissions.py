from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка на наличие прав администратора."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsAuthor(BasePermission):
    """Проверка, является ли пользователь владельцем или суперпользователем."""

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
