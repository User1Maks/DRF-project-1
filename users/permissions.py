from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    message = 'У Вас нет прав модератора.'

    def has_permission(self, request, view):
        """Проверяем пользователя на принадлежность к группе модераторов"""
        return request.user.groups.filter(name='moders').exists()


