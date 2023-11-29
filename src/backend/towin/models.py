from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.choices import TariffChoices, VenchiceTypeChoices
from django.contrib.auth import get_user_model

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
<<<<<<< HEAD
=======
    model_car = models.CharField(
        verbose_name="Модель и марка эвакуатора", max_length=255
    )
    license_plates = models.CharField(
        verbose_name="Гос. номер", max_length=10, validators=[plate_validator]
    )
>>>>>>> develop

    class Meta:
        verbose_name = "Эвакуатор"
        verbose_name_plural = "Эвакуаторы"

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

    def __str__(self) -> str:
        return self.name


class CarType(models.Model):
    car_type = models.CharField(
        "Тип машины", choices=VenchiceTypeChoices.choices
    )
    car_type_price = models.PositiveSmallIntegerField(
        verbose_name="Цена за тип авто",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Тип авто"
        verbose_name_plural = "Типы авто"
<<<<<<< HEAD
        default_related_name = "car_type"
=======
        constraints = [
            models.UniqueConstraint(
                fields=["car_type"], name="unique_car_type"
            )
        ]
>>>>>>> develop

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
<<<<<<< HEAD
=======
    )
    addition = models.CharField(
        verbose_name="Комментарий",
        max_length=300,
        null=True,
        blank=True,
    )
    delay = models.BooleanField(
        verbose_name="Задержка",
        default=False,
    )
    order_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        "Статус заказа", choices=Statuses.choices, default=Statuses.CREATED
    )
    price = models.ForeignKey(
        "PriceOrder", on_delete=models.SET_NULL, verbose_name="Цена", null=True
>>>>>>> develop
    )
    addition = models.CharField(verbose_name="Комментарий", max_length=300)
    delay = models.BooleanField(verbose_name="Задержка")
    tow_truck = models.ForeignKey(
<<<<<<< HEAD
        TowTruck, on_delete=models.CASCADE, verbose_name="Эвакуатор"
    )
    created = models.DateTimeField("Дата заказа", auto_now_add=True)

    class Meta:
=======
        TowTruck,
        on_delete=models.SET_NULL,
        verbose_name="Эвакуатор",
        null=True,
    )
    created = models.DateTimeField("Дата заказа", default=timezone.now)

    class Meta:
        ordering = ("-created",)
>>>>>>> develop
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        default_related_name = "orders"

    def __str__(self) -> str:
        return str(self.pk)


class PriceOrder(models.Model):
    """
    Модель Заказов и Цены. По логике должен
    связывать модель юзера и заказа.
    В итоге можно будет запрашивать
    все заказы пользователя.
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
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=0,
    )
    towin = models.BooleanField(verbose_name="Кюветные работы")
    order = models.ForeignKey(
<<<<<<< HEAD
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
=======
        Order, on_delete=models.CASCADE, verbose_name="Заказ", null=True
    )
    total = models.PositiveSmallIntegerField(
        verbose_name="Итоговая цена",
        default=0,
>>>>>>> develop
    )

    class Meta:
        ordering = ("order",)
        verbose_name = "Заказы и Цены"
        verbose_name_plural = "Заказы и цены"
        default_related_name = "price_orders"
        constraints = [
            models.UniqueConstraint(fields=["order"], name="unique_order")
        ]

    def __str__(self) -> str:
        return self.order


class Feedback(models.Model):
    """
    Модель оценки заказа.
    """

    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    comment = models.CharField(verbose_name="Комментарий", max_length=400)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
<<<<<<< HEAD
=======
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    ontime = models.BooleanField(
        verbose_name="Водитель приехал вовремя", default=True
    )
>>>>>>> develop

    class Meta:
        ordering = ("order",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
<<<<<<< HEAD

    def __str__(self) -> str:
        return self.order
=======
        default_related_name = "feedbacks"
        constraints = [
            models.UniqueConstraint(
                fields=["order"], name="unique_order_feedback"
            )
        ]

    def __str__(self) -> str:
        return str(self.pk)
>>>>>>> develop
