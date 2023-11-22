import random

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, permissions, status, response

from towin.models import Order, Feedback, TowTruck
from api.serializers import (
    UserSerializer,
    FeedbackSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
)

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """DjoserViewSet."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    token_generator = default_token_generator
    permission_classes = (permissions.AllowAny, )


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadOrderSerializer
        return CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Проверяем пользователя на авторизацию. Если авторизован создаем заказ.
        Если нет сохраняем введенные данные в сессию.
        """
        if request.user.is_authenticated:
            order_data = request.data
            order_data["price"]["car_type"] = order_data["car_type"][0]
            order_data["price"]["tariff"] = order_data["tariff"][0]
            order_data["tow_truck"] = self.get_random_tow_truck()

            serializer = CreateOrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["client"] = request.user
            serializer.save()

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        request.session["order_data"] = request.data

        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_random_tow_truck(self):
        """
        Возвращает случайный свободный эвакуатор
        """
        try:
            tow_trucks = TowTruck.objects.filter(is_active=True)
            return random.choice(tow_trucks)
        except TowTruck.DoesNotExist as e:
            raise e("Все эвакуаторы заняты :(")


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.AllowAny,)
