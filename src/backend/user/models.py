from typing import Any

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from phonenumber_field import modelfields
# from django.contrib.auth.models import AbstractUser
# from django.db import models

from user.utils import get_avatar_path


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User
    """

    def _create_user(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает и сохраняет юзера с почтой, телефоном, и паролем
        """
        if not email:
            raise ValueError('Электронная почта обязательна')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает юзера
        """

        return self._create_user(
            email,
            password,
            **extra_fields
        )

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает суперюзера
        """
        user = self._create_user(email, password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser):
    """
    Кастомная модель пользователя.
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone', 'first_name')

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    phone = modelfields.PhoneNumberField(
        'Телефон',
        region='RU',
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        error_messages={
            'unique': 'Этот адрес электронной почты уже зарегистрован.'
        }
    )
    is_verified = models.BooleanField(
        "Подтверждение",
        default=False
    )
    is_staff = models.BooleanField(
        'Стафф статус',
        default=False,
    )

    objects = MyUserManager()

    class Meta:
        ordering = ("email", "phone",)
        unique_together = ("email", "phone",)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.email

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Avatar(models.Model):
    user = models.OneToOneField(
        User,
        related_name='avatar',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Аватар',
        blank=True,
        null=True,
        upload_to=get_avatar_path,
    )

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватарки'
        ordering = ('user',)

    def __str__(self) -> str:
        return self.user.first_name
