from typing import Any

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from phonenumber_field import modelfields

from user.utils import get_avatar_path


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User
    """

    def _create_user(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает и сохраняет юзера c телефоном, и паролем
        """
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, phone: str, password: str, consent, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает юзера
        """
        if not consent:
            raise ValueError("Я не вижу согласия!")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("consent", consent)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает суперюзера
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    """

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ("first_name",)

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
    )
    phone = modelfields.PhoneNumberField(
        "Телефон",
        region="RU",
        unique=True,
        error_messages={
            "unique": "Пользователь с этим телефоном уже существует."
        },
    )
    consent = models.BooleanField(
        "Согласие на обработку данных и с политикой конфиденциальности",
        default=False,
    )
    is_active = models.BooleanField(
        "Активный пользователь",
        default=False,
    )
    is_staff = models.BooleanField(
        "Стафф статус",
        default=False,
    )
    is_superuser = models.BooleanField(
        "Super статус",
        default=False,
    )
    is_active = models.BooleanField(
        "Активный пользователь",
        default=False,
    )
    is_verified = models.BooleanField("Подтверждение", default=False)

    objects = MyUserManager()

    class Meta:
        ordering = ("phone",)
        unique_together = ("phone",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.phone} {self.first_name}"


class Avatar(models.Model):
    user = models.OneToOneField(
        User,
        related_name="avatar",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        "Аватар",
        blank=True,
        null=True,
        upload_to=get_avatar_path,
    )

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватарки"
        ordering = ("user",)

    def __str__(self) -> str:
        return self.user.first_name
