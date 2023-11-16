from django.db import models
from django.contrib.auth.models import AbstractUser
from core.choices import Roles


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        unique=True,
        max_length=254,
        db_index=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254,
        db_index=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Роль пользователя с правами доступа',
        max_length=30,
        choices=Roles.choices,
        default=Roles.USER
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN or self.is_superuser
