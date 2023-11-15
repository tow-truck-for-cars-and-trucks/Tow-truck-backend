# from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
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


class PriceOrderViewset(viewsets.ModelViewSet):
    queryset = PriceOrder.objects.all()
    serializer_class = PriceOrderSerializer
    permission_classes = (AllowAny,)


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)
