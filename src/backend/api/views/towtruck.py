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

from api.filters import OrderFilter

from api.serializers.towtruck import (
    FeedbackCreateSerializer,
    FeedbackReadSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
    TariffSerializer,
    CarTypeSerializer,
    TowTruckSerializer,
)
from api.permissions import IsAdminOrReadOnly
from towin.models import Order, Feedback, TowTruck, CarType, Tariff


User = get_user_model()


class OrderViewset(viewsets.ModelViewSet):
    filterset_class = OrderFilter

    def get_queryset(self):
        client = self.request.user.id
        return Order.objects.filter(client=client)

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
        if request.user.is_authenticated:
            order_data = request.data
            order_data["price"]["car_type"] = order_data["car_type"]
            order_data["price"]["tariff"] = order_data["tariff"]
            order_data["delivery_time"] = Order.get_delivery_time(
                self, tariff_id=order_data["tariff"]
            )

            serializer = CreateOrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["client"] = request.user
            serializer.save()

            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
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
                if instance.status == "Активный":
                    instance.tow_truck = self.get_random_tow_truck()
                    instance.tow_truck.is_active = True
                else:
                    instance.tow_truck.is_active = False
                instance.save(update_fields=["status", "tow_truck"])
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
            tow_trucks = TowTruck.objects.filter(is_active=False)
            return random.choice(tow_trucks)
        except TowTruck.DoesNotExist as e:
            raise e("Все эвакуаторы заняты :(")


class FeedbackViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        if self.action == "list":
            return Feedback.objects.exclude(comment__isnull=True)
        return Feedback.objects.all()

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


class TowTruckViewset(viewsets.ModelViewSet):
    queryset = TowTruck.objects.all()
    serializer_class = TowTruckSerializer
    permission_classes = (IsAdminOrReadOnly,)
