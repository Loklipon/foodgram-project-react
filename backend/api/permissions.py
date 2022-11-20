from rest_framework import permissions


class IsAuthorOrIsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений для модели с рецептами.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class AccessDenied(permissions.BasePermission):
    """
    Класс разрешений для закрытия доступа
    к неиспользуемым эндпоинтам приложения djoser.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
