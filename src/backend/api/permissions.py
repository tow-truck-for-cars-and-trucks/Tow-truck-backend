from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверяет является ли запрос безопасным или является
    ли автор запроса суперпользователя. В случае прохождения
    проверки отправляет True, иначе False.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )


class IsSelfUserOrAdmin(permissions.BasePermission):
    """
    Проверяет является ли автор запроса владельцем аккаунта запроса или
    является ли суперпользователем/админом. В случае прохождения
    проверки отправляет True, иначе False.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_anonymous or user.is_superuser or user == obj
        )
