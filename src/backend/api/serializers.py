from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback, CarType
from user.models import User


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


class PriceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceOrder
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = "__all__"


class ReadOrderSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    price = PriceOrderSerializer(read_only=True)
    wheel_lock = serializers.IntegerField(
        source='price.wheel_lock',
        read_only=True
    )
    towin = serializers.BooleanField(
        source='price.towin',
        read_only=True,
    )
    tariff = TariffSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'client',
            'address_from',
            'address_to',
            'car_type',
            'wheel_lock',
            'towin',
            'addition',
            'tariff',
            'price',
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    car_tape = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CarType.objects.all()
    )
    client = UserSerializer(read_only=True, required=False)
    price = PriceOrderSerializer(read_only=True)
    wheel_lock = serializers.IntegerField(source='price.wheel_lock')
    towin = serializers.BooleanField(source='price.towin')
    tariff = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tariff.objects.all()
    )

    class Meta:
        model = Order
        fields = (
            'client',
            'address_from',
            'address_to',
            'car_type',
            'wheel_lock',
            'towin',
            'tariff',
            'delay',
            'addition',
            'price',
        )
