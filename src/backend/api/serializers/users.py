from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации и получения подробной информации
    о пользователе.
    """

    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        "password_mismatch": "Пароли не совпадают",
        "re_password": "Отсутствует поле re_password в теле запроса.",
    }

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "phone",
            "consent",
            "password",
            "re_password",
        )

    def validate(self, attrs):
        """
        Добавлена валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        try:
            self.fields.pop("re_password")
            re_password = attrs.pop("re_password")
            password = attrs["password"]
        except KeyError:
            return self.fail("re_password")
        if re_password == password:
            user = User(**attrs)
            validate_password(password, user)
            return attrs
        return self.fail("password_mismatch")

    def create(self, validated_data):
        """
        Вызывает создание обычного юзера.
        """
        consent = validated_data.pop("consent")
        if not consent:
            raise serializers.ValidationError("Я не вижу согласия!")
        return User.objects.create_user(consent=consent, **validated_data)


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
            "first_name",
            "phone",
            "image",
        )
