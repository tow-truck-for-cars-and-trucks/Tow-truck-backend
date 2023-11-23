import random

from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, response, mixins

from towin.models import Order, Feedback, TowTruck, CarType, Tariff
from api.serializers.towtruck import (
    FeedbackCreateSerializer,
    FeedbackReadSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
    TariffSerializer,
    CarTypeSerializer
)
from api.permissions import IsAdminOrReadOnly

User = get_user_model()


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOrderSerializer
        return CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Проверяем пользователя на авторизацию. Если авторизован создаем заказ.
        Если нет сохраняем введенные данные в сессию.
        """
        if request.user.is_authenticated:
            order_data = request.data
            order_data['price']['car_type'] = order_data['car_type'][0]
            order_data['price']['tariff'] = order_data['tariff'][0]
            order_data['tow_truck'] = self.get_random_tow_truck()

            serializer = CreateOrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['client'] = request.user
            serializer.save()

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        request.session['order_data'] = request.data

        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_random_tow_truck(self):
        """
        Возвращает случайный свободный эвакуатор
        """
        try:
            tow_trucks = TowTruck.objects.filter(is_active=True)
            return random.choice(tow_trucks)
        except TowTruck.DoesNotExist as e:
            raise e('Все эвакуаторы заняты :(')


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FeedbackReadSerializer
        return FeedbackCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(name=self.request.user)

    def _feedback_post_method(self, request, FeedbackCreateSerializer):
        data = request.POST.copy()
        data.update({'name': request.user})
        serializer = FeedbackCreateSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class CarTypeViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TariffViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = (IsAdminOrReadOnly,)
