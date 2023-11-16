from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from towin.models import (
    TowTruck,
    Tariff,
    Order,
    PriceOrder,
    Feedback,
    CarType,
    User # лучше импортировать из towin.models потому что там один раз вызываеться метод который обращается к "AUTH_USER_MODEL" комент можно удалить )
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
        fields = ('car_type', 'price')


class ReadOrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
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
    client = CustomUserSerializer(read_only=True, required=False)
    price = PriceOrderSerializer()

    car_type = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CarType.objects.all()
    )
    # wheel_lock = serializers.IntegerField(source='price.wheel_lock')
    # towin = serializers.BooleanField(source='price.towin')
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
            # 'wheel_lock',
            # 'towin',
            'tariff',
            'delay',
            'addition',
            'price',
        )

    def create(self, validated_data):
        price_data = validated_data.pop('price')
        car_type_data = validated_data.pop('car_type')
        tariff_data = validated_data.pop('tariff')
        order = Order.objects.create(**validated_data)
        order_price_data = price_data.pop('order')
        price_order = PriceOrder.objects.create(**order_price_data)

        order.price = price_order
        order.save()

        for car_type in car_type_data:
            order.car_type.add(car_type)

        for tariff in tariff_data:
            order.tariff.add(tariff)

        return order
