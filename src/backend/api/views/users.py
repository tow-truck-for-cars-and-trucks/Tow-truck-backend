
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from api.serializers.users import UserSerializer


User = get_user_model()


class UserViewset(DjoserUserViewSet):
    """DjoserViewSet."""
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    token_generator = default_token_generator
