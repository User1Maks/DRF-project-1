from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяем пользователя на принадлежность к владельцу объекта"""

        if obj.owner == request.user:
            return True
        return False
