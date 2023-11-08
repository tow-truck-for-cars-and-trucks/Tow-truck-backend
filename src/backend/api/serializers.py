from rest_framework import serializers


from user.models import User
from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя как <Наниматель>."""

    class Meta:
        model = User
        fields = "__all__"


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
