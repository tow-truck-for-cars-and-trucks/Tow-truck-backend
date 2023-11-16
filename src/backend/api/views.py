# from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions

# from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


from user.models import User
from towin.models import Order, Feedback
from api.serializers import (
    # TowTruckSerializer,
    # TariffSerializer,
    # PriceOrderSerializer,
    FeedbackSerializer,
    CustomUserSerializer,
    ReadOrderSerializer,
    CreateOrderSerializer,
)


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOrderSerializer
        return CreateOrderSerializer


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)
