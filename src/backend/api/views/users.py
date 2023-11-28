from rest_framework import permissions, response, status
from djoser.views import UserViewSet as DjoserUserViewSet

from api.serializers.users import UserSerializer

from backend.user.models import User


class UserViewset(DjoserUserViewSet):
    """DjoserViewSet."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(
            {"message": "Пользователь успешно удален"},
            status=status.HTTP_200_OK,
        )
