from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from djoser.compat import get_user_email, get_user_email_field_name
# from djoser.conf import settings

from towin.models import TowTruck, Tariff, Order, PriceOrder, Feedback, CarType
# from user.models import User
from api.utils.fields import LowercaseEmailField


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
    default_error_messages = {
        'password_mismatch': 'Пароли не совпадают'
    }

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            're_password',
        )

    def validate(self, attrs):
        """
        Добавлена валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        self.fields.pop('re_password')
        re_password = attrs.pop('re_password')
        password = attrs['password']
        if re_password == password:
            user = User(**attrs)
            validate_password(password, user)
            return attrs
        return self.fail('password_mismatch')

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
    image = serializers.ImageField(read_only=True, source='avatar.image')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'image',
        )
        read_only_fields = ('email', 'is_subscribed')


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
        'password_mismatch': 'Новый пароль не совпадает с повторным вводом',
        'invalid_password': 'Текущий пароль не верный'
    }

    def validate_current_password(self, value):
        """
        Валидация текущего пароля.
        """
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop('re_password')
        password = attrs['password']
        user = self.context['request'].user
        if re_password == password:
            validate_password(password, user)
            return attrs
        return self.fail('password_mismatch')


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор для установки нового пароля после сброса.
    """
    email = LowercaseEmailField()
    confirmation_code = serializers.IntegerField()
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        'password_mismatch': 'Новый пароль не совпадает с повторным вводом',
    }

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop('re_password')
        password = attrs['password']
        if re_password == password:
            validate_password(password, User(email=attrs['email']))
            return attrs
        return self.fail('password_mismatch')


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
    car_type = serializers.PrimaryKeyRelatedField(
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
