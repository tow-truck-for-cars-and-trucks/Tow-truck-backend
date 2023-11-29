from rest_framework import permissions, response, status
from djoser.views import UserViewSet as DjoserUserViewSet

from api.permissions import IsSelfUserOrAdmin
from api.serializers.users import UserSerializer

from user.models import User


class UserViewset(DjoserUserViewSet):
    """DjoserViewSet."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'partial_update', 'update',):
            permission_classes = (IsSelfUserOrAdmin,)
        elif self.action in ('create',):
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(
            {"message": "Пользователь успешно удален"},
            status=status.HTTP_200_OK,
        )
