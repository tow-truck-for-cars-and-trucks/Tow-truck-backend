from rest_framework import serializers

from core.functions import avg_towtruck_score
from towin.models import (
    TowTruck,
    Tariff,
    Order,
    PriceOrder,
    Feedback,
    CarType,
)
from api.serializers.users import UserSerializer


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


class FeedbackCreateSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ('id', 'score', 'comment', 'order', 'name', 'ontime')

    def get_name(self, obj):
        request = self.context.get('request')
        name = request.user.first_name
        return name


class FeedbackReadSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.first_name')

    class Meta:
        model = Feedback
        fields = ('id', 'score', 'comment', 'order', 'name', 'ontime')


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ('car_type', 'price')


class ReadOrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(
        read_only=True
    )
    price = PriceOrderSerializer()
    car_type = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='price.car_type'
    )
    wheel_lock = serializers.PrimaryKeyRelatedField(
        source='price.wheel_lock',
        read_only=True
    )
    towin = serializers.BooleanField(
        source='price.towin',
        read_only=True,
    )
    tariff = serializers.PrimaryKeyRelatedField(
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
            'order_date',
            'status',
            'price',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = instance.price.total
        return representation


class CreateOrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(
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
            'order_date',
            'status',
            'addition',
            'price',
        )

    def to_representation(self, instance):
        return ReadOrderSerializer(instance, context={
            'request': self.context.get('request')
        }).data

    def create(self, validated_data):

        if validated_data.get('delay', False):
            validated_data['order_date'] = self.initial_data.get(
                'order_date', None
            )

        price_data = validated_data.pop('price')
        order_instance = Order.objects.create(**validated_data)

        if price_data:
            price_order_instance = PriceOrder.objects.create(
                order=order_instance, **price_data)
            order_instance.price = price_order_instance
            order_instance.save()

        return order_instance
