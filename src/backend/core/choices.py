from django.db import models


class Roles(models.TextChoices):
    """
    Типы возможных ролей для пользователей.
    """

    USER = "User", "Пользователь"
    ADMIN = "Admin", "Администратор"


class Statuses(models.TextChoices):
    """
    Типы статуса заказа.
    """

    CREATED = "Созданный", "Созданный"
    ACTIVE = "Активный", "Активный"
    COMPLETED = "Завершенный", "Завершенный"
    CANCELED = "Отмененный", "Отмененный"


class TariffChoices(models.TextChoices):
    """
    Класс выбора тарифа.
    """

    ECONOM = "Эконом", "Эконом"
    EXPRESS = "Экспресс", "Экспресс"
    MANIPULATOR = "Манипулятор", "Манипулятор"


class VenchiceTypeChoices(models.TextChoices):
    """
    Класс выбора типа транспорта.
    """

    CAR = "Легковой", "Легковой"
    TRUCK = "Грузовой", "Грузовой"
    MOTO = "Мотоцикл", "Мотоцикл"
    SPECIAL = "Спецтехника", "Спецтехника"
