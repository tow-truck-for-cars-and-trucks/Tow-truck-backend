from django.db import models


class Roles(models.TextChoices):
    """
    Типы возможных ролей для пользователей.
    """

    USER = 'User', 'Пользователь'
    ADMIN = 'Admin', 'Администратор'


class TariffChoices(models.TextChoices):
    """
    Класс выбора тарифа.
    """
    ECONOM = 'Econom', 'Эконом'
    EXPRESS = 'Express', 'Экспресс'
    MANIPULATOR = 'Manipulator', 'Манипулятор'


class VenchiceTypeChoices(models.TextChoices):
    """
    Класс выбора типа транспорта.
    """
    SEDAN = 'Sedan', 'Седан'
    HATCHBACK = 'Hatchback', 'Хетчбек'
    MINIVAN = 'Minivan', 'Минивен'
    CABRIOLET = 'Cabriolet', 'Кабриолет'
    SPORTCAR = 'Sportcar', 'Спорткар'
    PICKUP = 'Pickup', 'Пикап'
    WD = 'WD', 'Внедорожник'
    MOTO = 'Moto', 'Мотоцикл'
