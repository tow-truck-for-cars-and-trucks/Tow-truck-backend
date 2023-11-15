from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer


from user.models import User
from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback


class CustomUserSerializer(UserSerializer):
    """Сериализатор модели пользователя как <Наниматель>."""

    class Meta:
        model = User
        fields = (
            "email",
            "tel",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "id",
            "password",
            "email",
            "tel",
            "first_name",
            "last_name",
        )


class TowTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = TowTruck
        fields = "__all__"


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class PriceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceOrder
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
