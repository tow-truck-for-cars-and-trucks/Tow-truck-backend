from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.functions import avg_towtruck_score
from towin.models import (
    TowTruck,
    Tariff,
    Order,
    PriceOrder,
    Feedback,
    CarType,
    User
)


class CustomUserSerializer(UserSerializer):
    """Сериализатор модели пользователя как <Наниматель>."""

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
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
            "phone",
            "first_name",
            "last_name",
        )


class TowTruckSerializer(serializers.ModelSerializer):
    avarage_score = serializers.SerializerMethodField()

    class Meta:
        model = TowTruck
        fields = (
            "is_active",
            "driver",
            "model_car",
            "license_plates",
            "avarage_score",
        )

    def get_avarage_score(self, obj):
        return avg_towtruck_score(obj)


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
        fields = ('car_type', 'price')


class ReadOrderSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(
        read_only=True
    )
    price = PriceOrderSerializer()
    car_type = serializers.StringRelatedField(
        read_only=True,
        source='price.car_type'
    )
    wheel_lock = serializers.IntegerField(
        source='price.wheel_lock',
        read_only=True
    )
    towin = serializers.BooleanField(
        source='price.towin',
        read_only=True,
    )
    tariff = serializers.StringRelatedField(
        source='price.tariff',
        read_only=True
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
            'addition',
            'tariff',
            'price',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = instance.price.total
        return representation


class CreateOrderSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(
        read_only=True,
        required=False
    )
    price = PriceOrderSerializer()
    car_type = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CarType.objects.all(),
        source='price.car_type'
    )
    tariff = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tariff.objects.all(),
        source='price.tariff'
    )

    class Meta:
        model = Order
        fields = (
            'client',
            'address_from',
            'address_to',
            'car_type',
            'tariff',
            'delay',
            'addition',
            'price',
        )


    def to_representation(self, instance):
        return ReadOrderSerializer(instance, context={
            'request': self.context.get('request')
        }).data

    def create(self, validated_data):
        price_data = validated_data.pop('price')
        order_instance = Order.objects.create(**validated_data)

        if price_data:
            price_order_instance = PriceOrder.objects.create(
                order=order_instance, **price_data)
            order_instance.price = price_order_instance
            order_instance.save()

        return order_instance
