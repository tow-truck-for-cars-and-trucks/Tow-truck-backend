# from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
# from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from user.models import User
from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback
from api.serializers import (
    TowTruckSerializer,
    TariffSerializer,
    PriceOrderSerializer,
    FeedbackCreateSerializer,
    FeedbackReadSerializer,
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
    permission_classes = (AllowAny,)

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
