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
    ECONOM = 'Эконом', 'Эконом'
    EXPRESS = 'Экспресс', 'Экспресс'
    MANIPULATOR = 'Манипулятор', 'Манипулятор'


class VenchiceTypeChoices(models.TextChoices):
    """
    Класс выбора типа транспорта.
    """
    SEDAN = 'Седан', 'Седан'
    HATCHBACK = 'Хетчбек', 'Хетчбек'
    MINIVAN = 'Минивен', 'Минивен'
    CABRIOLET = 'Кабриолет', 'Кабриолет'
    SPORTCAR = 'Спорткар', 'Спорткар'
    PICKUP = 'Пикап', 'Пикап'
    WD = 'Внедорожник', 'Внедорожник'
    MOTO = 'Мотоцикл', 'Мотоцикл'
