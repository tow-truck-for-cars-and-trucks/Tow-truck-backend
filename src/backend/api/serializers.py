from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from djoser.compat import get_user_email, get_user_email_field_name
# from djoser.conf import settings

from api.utils.fields import LowercaseEmailField

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework import serializers

from core.functions import avg_towtruck_score
from towin.models import (
    TowTruck,
    Tariff,
    Order,
    PriceOrder,
    Feedback,
    CarType,
    # User
)


User = get_user_model()


# class UserSerializer(UserSerializer):
#     """Сериализатор модели пользователя."""

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "email",
#             "phone",
#             "username",
#             "first_name",
#             "last_name",
#             "password",
#         )

#     def update(self, instance, validated_data):
#         email_field = get_user_email_field_name(User)
#         instance.email_changed = False
#         if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
#             instance_email = get_user_email(instance)
#             if instance_email != validated_data[email_field]:
#                 instance.is_active = False
#                 instance.email_changed = True
#                 instance.save(update_fields=["is_active"])
#         return super().update(instance, validated_data)


# class UserCreateSerializer(UserCreateSerializer):
#     """Сериализатор создания пользователя."""

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "email",
#             "phone",
#             "username",
#             "password",
#         )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации и получения подробной информации
    о пользователе.
    """

    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {"password_mismatch": "Пароли не совпадают"}

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "re_password",
        )

    def validate(self, attrs):
        """
        Добавлена валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        self.fields.pop("re_password")
        re_password = attrs.pop("re_password")
        password = attrs["password"]
        if re_password == password:
            user = User(**attrs)
            validate_password(password, user)
            return attrs
        return self.fail("password_mismatch")

    def create(self, validated_data):
        """
        Вызывает создание обычного юзера.
        """
        return User.objects.create_user(**validated_data)


class UserMeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения пользователем данных о себе
    и их изменения.
    """

    image = serializers.ImageField(read_only=True, source="avatar.image")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "image",
        )
        read_only_fields = ("email", "is_subscribed")


class EmailSerializer(serializers.Serializer):
    """
    Сериализатор c полем email.
    """

    email = LowercaseEmailField()


class SendCodeSerializer(EmailSerializer):
    """
    Сериализатор для отправки кода подтверждения.
    """

    pass


class ConfirmationCodeSerializer(EmailSerializer):
    """
    Сериализатор для активации пользователя через
    ввод кода подтверждения с эл. почты.
    """

    confirmation_code = serializers.IntegerField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для смены пароля юзера.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    current_password = serializers.CharField(write_only=True, max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        "password_mismatch": "Новый пароль не совпадает с повторным вводом",
        "invalid_password": "Текущий пароль не верный",
    }

    def validate_current_password(self, value):
        """
        Валидация текущего пароля.
        """
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop("re_password")
        password = attrs["password"]
        user = self.context["request"].user
        if re_password == password:
            validate_password(password, user)
            return attrs
        return self.fail("password_mismatch")


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор для установки нового пароля после сброса.
    """

    email = LowercaseEmailField()
    confirmation_code = serializers.IntegerField()
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        "password_mismatch": "Новый пароль не совпадает с повторным вводом",
    }

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop("re_password")
        password = attrs["password"]
        if re_password == password:
            validate_password(password, User(email=attrs["email"]))
            return attrs
        return self.fail("password_mismatch")


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
        fields = ("car_type", "price")


class ReadOrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    price = PriceOrderSerializer()
    car_type = serializers.StringRelatedField(read_only=True, source="price.car_type")
    wheel_lock = serializers.IntegerField(source="price.wheel_lock", read_only=True)
    towin = serializers.BooleanField(
        source="price.towin",
        read_only=True,
    )
    tariff = serializers.StringRelatedField(source="price.tariff", read_only=True)

    class Meta:
        model = Order
        fields = (
            "client",
            "address_from",
            "address_to",
            "car_type",
            "wheel_lock",
            "towin",
            "addition",
            "tariff",
            "price",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["price"] = instance.price.total
        return representation


class CreateOrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True, required=False)
    price = PriceOrderSerializer()
    car_type = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CarType.objects.all(), source="price.car_type"
    )
    tariff = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tariff.objects.all(), source="price.tariff"
    )

    class Meta:
        model = Order
        fields = (
            "client",
            "address_from",
            "address_to",
            "car_type",
            "tariff",
            "delay",
            "addition",
            "price",
        )

    def to_representation(self, instance):
        return ReadOrderSerializer(
            instance, context={"request": self.context.get("request")}
        ).data

    def create(self, validated_data):
        price_data = validated_data.pop("price")
        order_instance = Order.objects.create(**validated_data)

        if price_data:
            price_order_instance = PriceOrder.objects.create(
                order=order_instance, **price_data
            )
            order_instance.price = price_order_instance
            order_instance.save()

        return order_instance
