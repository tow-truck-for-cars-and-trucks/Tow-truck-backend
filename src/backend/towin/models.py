from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


from datetime import timedelta

from core.choices import TariffChoices, VenchiceTypeChoices, Statuses
from core.validators import plate_validator

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
    model_car = models.CharField(
        verbose_name="Модель и марка эвакуатора", max_length=255
    )
    license_plates = models.CharField(
        verbose_name="Гос. номер", max_length=10, validators=[plate_validator]
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
    delivery_time = models.TimeField("Время подачи", null=True)

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
        User,
        verbose_name="Пользователь",
        on_delete=models.SET_NULL,
        null=True,
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
        default=False,
    )
    order_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        "Статус заказа", choices=Statuses.choices, default=Statuses.CREATED
    )
    price = models.ForeignKey(
        "PriceOrder", on_delete=models.SET_NULL, verbose_name="Цена", null=True
    )
    tow_truck = models.ForeignKey(
        TowTruck,
        on_delete=models.SET_NULL,
        verbose_name="Эвакуатор",
        null=True,
    )
    created = models.DateTimeField("Дата заказа", default=timezone.now)
    delivery_time = models.DateTimeField(
        "Время подачи",
        help_text=(
            'В случае если заказ "Отложенный",'
            " укажите здесь дату и время подачи."
        ),
        default=timezone.now,
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        default_related_name = "orders"

    def __str__(self) -> str:
        return str(self.pk)

    def get_delivery_time(self, tariff_id):
        """
        На основе тарифа определяет время подачи машины.
        """
        tariff_time = Tariff.objects.get(pk=tariff_id)
        value = timezone.now() + timedelta(
            hours=int(tariff_time.delivery_time.hour),
            minutes=int(tariff_time.delivery_time.minute),
            seconds=int(tariff_time.delivery_time.second),
        )
        return value

    get_delivery_time.short_description = "Время подачи эвакуатора"

    def save(self, *args, **kwargs):
        """
        Переопределение метода необходимо
        для того, чтобы строка delivery_time
        принимала значение из функции
        калькуляции стоимости заказа.
        """

        try:
            Order.objects.get(pk=self.id)
            self.delivery_time = self.get_delivery_time(self.price.tariff.id)
        except ObjectDoesNotExist:
            pass

        super(Order, self).save(*args, **kwargs)

    def clean(self) -> None:
        """
        Валидация значения времени подачи эвакуатора и создания заказа.
        Если значение указано в прошлом, то выбрасывает ошибку.
        """

        time = self.created + timedelta(minutes=10)

        if time < timezone.now():
            raise ValidationError("Заказ не может быть создан в прошлом.")

        if time < timezone.now():
            raise ValidationError("Время/дата подачи не может быть в прошлом!")


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
        null=True,
    )
    total = models.PositiveSmallIntegerField(
        verbose_name="Итоговая цена",
        default=0,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "Заказы и Цены"
        verbose_name_plural = "Заказы и цены"
        default_related_name = "price_orders"
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
        принимала значение из функции
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
    )
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    ontime = models.BooleanField(
        verbose_name="Водитель приехал вовремя", default=True
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации отзыва", default=timezone.now
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = "feedbacks"
        constraints = [
            models.UniqueConstraint(
                fields=["order"], name="unique_order_feedback"
            ),
            models.UniqueConstraint(
                fields=["name"], name="unique_user_feedback"
            ),
        ]

    def __str__(self) -> str:
        return str(self.pk)
