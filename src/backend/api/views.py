import random

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from towin.models import Order, Feedback, TowTruck, User
from api.serializers import (
    # TowTruckSerializer,
    # TariffSerializer,
    # PriceOrderSerializer,
    FeedbackSerializer,
    CustomUserSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
)


class CustomUserViewset(DjoserUserViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = LimitPageNumberPagination

    # Если юзер пришел с оформления заказа он регестрируеться, после чего
    # берем данные из сессии добавляем id user в данные и предаем в сериализатор
    # проверяем и сохраняем
    # order_data = request.session.get('order_data', {})
    # order_data['client'] = user.id  # Предполагается, что user - это объект пользователя
    # serializer = CreateOrderSerializer(data=order_data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        request.session['order_data'] = request.data

        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

# class CarTypeViewset(viewsets.ModelViewSet):
#     queryset = CarType.objects.all()
#     serializer_class = CarTypeSerializer
