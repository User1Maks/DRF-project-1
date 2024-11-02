from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    message = 'У Вас нет прав модератора.'

    def has_permission(self, request, view):
        """Проверяем пользователя на принадлежность к группе модераторов"""
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяем пользователя на принадлежность к владельцу объекта"""

        if obj.owner == request.user:
            return True
        return False
