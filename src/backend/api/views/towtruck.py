import random

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import (
    viewsets,
    permissions,
    status,
    response,
    mixins,
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.serializers.towtruck import (
    FeedbackCreateSerializer,
    FeedbackReadSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
    TariffSerializer,
    CarTypeSerializer,
)
from api.permissions import IsAdminOrReadOnly
from towin.models import Order, Feedback, TowTruck, CarType, Tariff

User = get_user_model()


class OrderViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        status = self.request.query_params.get("status", "Созданный")
        client = self.request.user
        return Order.objects.filter(client=client).filter(status=status)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadOrderSerializer
        return CreateOrderSerializer

    @action(methods=("POST",), permission_classes=(AllowAny,), detail=False)
    def total_price(self, request, **kwargs):
        order_data = request.data
        car_tape = CarType.objects.get(id=order_data["car_type"]).price
        tariff_id = Tariff.objects.get(id=order_data["tariff"]).price
        wheel_lock = (
            order_data["price"]["wheel_lock"] * settings.WHEEL_LOCK_PRICE
        )
        towin_price = (
            settings.TOWIN_PRICE if order_data["price"]["towin"] else False
        )
        total = sum([car_tape, tariff_id, wheel_lock, towin_price])
        context = {"price": total}
        return response.Response(context, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Проверяем пользователя на авторизацию. Если авторизован создаем заказ.
        Если нет сохраняем введенные данные в сессию.
        """
        if request.user.is_authenticated:
            order_data = request.data
            order_data["price"]["car_type"] = order_data["car_type"]
            order_data["price"]["tariff"] = order_data["tariff"]
            order_data["tow_truck"] = self.get_random_tow_truck()

            serializer = CreateOrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["client"] = request.user
            serializer.save()

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        # request.session['order_data'] = request.data

        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        """
        Обновление статуса заказа.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            if "status" in request.data:
                instance.status = request.data["status"]
                instance.save(update_fields=["status"])
                return response.Response(serializer.data)
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

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
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FeedbackReadSerializer
        return FeedbackCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(name=self.request.user)

    def _feedback_post_method(self, request, FeedbackCreateSerializer):
        data = request.POST.copy()
        data.update({"name": request.user})
        serializer = FeedbackCreateSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid()
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class CarTypeViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TariffViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = (IsAdminOrReadOnly,)