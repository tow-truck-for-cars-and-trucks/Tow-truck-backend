# from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


from user.models import User
from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback
from api.serializers import (
    TowTruckSerializer,
    TariffSerializer,
    PriceOrderSerializer,
    FeedbackSerializer,
    UserSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
)


class UserViewset(DjoserUserViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
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


class TowTruckViewset(viewsets.ModelViewSet):
    queryset = TowTruck.objects.all()
    serializer_class = TowTruckSerializer
    permission_classes = (AllowAny,)


class TariffViewset(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = (AllowAny,)


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
            serializer = CreateOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['client'] = request.user
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        request.session['order_data'] = request.data
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PriceOrderViewset(viewsets.ModelViewSet):
    queryset = PriceOrder.objects.all()
    serializer_class = PriceOrderSerializer
    permission_classes = (AllowAny,)


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)


# class CarTypeViewset(viewsets.ModelViewSet):
#     queryset = CarType.objects.all()
#     serializer_class = CarTypeSerializer
