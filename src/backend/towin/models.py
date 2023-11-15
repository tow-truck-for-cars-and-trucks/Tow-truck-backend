from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.choices import TariffChoices, VenchiceTypeChoices


User = get_user_model()


class TowTruck(models.Model):
    """
    Модель эвакуатора.
    """

    is_active = models.BooleanField(
        verbose_name="Статус эвакуатора.",
    )
    driver = models.CharField(
        verbose_name="Водитель",
        help_text="Укажите водителя",
        max_length=255,
    )

    class Meta:
        verbose_name = "Эвакуатор"
        verbose_name_plural = "Эвакуаторы"
        constraints = [
            models.UniqueConstraint(fields=["driver"], name="unique_driver")
        ]

    def __str__(self) -> str:
        return self.driver


class Tariff(models.Model):
    """
    Модель тарифа.
    """

    name = models.CharField(
        verbose_name="Название тарифа",
        max_length=50,
        choices=TariffChoices.choices,
    )
    description = models.CharField(
        verbose_name="Описание тарифа", max_length=255
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена тарифа", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_tariff_name")
        ]

    def __str__(self) -> str:
        return self.name


class CarType(models.Model):
    """
    Модель типа автомобиля.
    """

    car_type = models.CharField(
        "Тип машины", choices=VenchiceTypeChoices.choices
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена за тип авто",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Тип авто"
        verbose_name_plural = "Типы авто"
        default_related_name = "car_type"
        constraints = [
            models.UniqueConstraint(
                fields=["car_type"], name="unique_car_type"
            )
        ]

    def __str__(self):
        return self.car_type


class Order(models.Model):
    """
    Модель заказа.
    """

    client = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    address_from = models.CharField(
        verbose_name="Адрес подачи", max_length=200
    )
    address_to = models.CharField(
        verbose_name="Адрес прибытия", max_length=200
    )
    addition = models.CharField(
        verbose_name="Комментарий",
        max_length=300,
        null=True,
        blank=True,
    )
    delay = models.BooleanField(
        verbose_name="Задержка",
    )
    tow_truck = models.ForeignKey(
        TowTruck, on_delete=models.CASCADE, verbose_name="Эвакуатор"
    )
    created = models.DateTimeField("Дата заказа", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return str(self.pk)


class PriceOrder(models.Model):
    """
    Модель Заказов и Цены. По логике должен
    связывать модель юзера и заказа.
    В итоге можно будет запрашивать
    все заказы пользователя.
    По своей сути является составом заказа.
    """

    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name="Тариф",
        max_length=30,
    )
    car_type = models.ForeignKey(
        CarType,
        on_delete=models.CASCADE,
        verbose_name="Тип авто",
        max_length=30,
    )
    wheel_lock = models.PositiveSmallIntegerField(
        verbose_name="Заблокированные колеса",
        validators=[MaxValueValidator(4)],
        default=0,
    )
    towin = models.BooleanField(verbose_name="Кюветные работы")
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
    total = models.PositiveSmallIntegerField(
        verbose_name="Итоговая цена",
        default=0,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "Заказы и Цены"
        verbose_name_plural = "Заказы и цены"

        constraints = [
            models.UniqueConstraint(fields=["order"], name="unique_order")
        ]

    def __str__(self) -> str:
        return str(self.order)

    def calculate_total(self):
        """
        Функция подсчета итоговой стоимости заказа.
        """

        tariff_price = self.tariff.price
        car_type_price = self.car_type.price
        wheel_lock_price = self.wheel_lock * settings.WHEEL_LOCK_PRICE
        if self.towin:
            towin_price = settings.TOWIN_PRICE
        else:
            towin_price = 0

        total = tariff_price + car_type_price + wheel_lock_price + towin_price

        return total

    calculate_total.short_description = "Стоимость"

    def save(self, *args, **kwargs):
        """
        Переопределение метода необходимо
        для того, чтобы строка total
        принимало значение из функции
        калькуляции стоимости заказа.
        """

        self.total = self.calculate_total()
        super(PriceOrder, self).save(*args, **kwargs)


class Feedback(models.Model):
    """
    Модель оценки заказа.
    """

    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MaxValueValidator(5)],
    )
    comment = models.CharField(
        verbose_name="Комментарий",
        max_length=400,
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="score",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("order",)
        constraints = [
            models.UniqueConstraint(
                fields=["order"], name="unique_order_feedback"
            )
        ]

    def __str__(self) -> str:
        return self.order
