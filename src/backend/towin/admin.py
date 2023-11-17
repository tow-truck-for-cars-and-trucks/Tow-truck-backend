from django.contrib import admin
from core.models import MinValidatedInlineMixIn
from core.models import EmptyFieldModel
from .models import Order, Feedback, TowTruck, Tariff, PriceOrder, CarType
from django.db.models import Avg


class OrderriceTabularInline(admin.TabularInline, MinValidatedInlineMixIn):
    model = PriceOrder
    validate_min = True
    min_num = 1


class OdrderAdmin(EmptyFieldModel):
    list_display = (
        "id",
        "client",
        "address_from",
        "address_to",
        "created",
        "addition",
        "delay",
        "tow_truck",
        "total_price",
    )
    search_fields = ('address_from', 'address_to',)
    readonly_fields = ('total_price',)
    inlines = [OrderriceTabularInline]

    def total_price(self, instance):
        return PriceOrder.objects.get(order=instance).total

    total_price.short_description = 'Итоговая стоимость'


class FeedbackAdmin(EmptyFieldModel):
    list_display = ("order", "score", "comment")


class TowTruckAdmin(EmptyFieldModel):
    list_display = (
        "id",
        "is_active",
        "driver",
        "model_car",
        "license_plates",
        'avg_score'
    )

    def avg_score(self, instance):
        """
        Рассчет средней оценки эвакуатора.
        """

        scores = Feedback.objects.filter(order__tow_truck=instance)
        if not scores:
            return None

        return scores.aggregate(Avg('score'))['score__avg']

    avg_score.short_description = 'Средняя оценка'


class TariffAdmin(EmptyFieldModel):
    list_display = ("name", "description", "price")


class CarTypeAdmin(EmptyFieldModel):
    list_display = ("car_type", "price")


admin.site.register(Order, OdrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TowTruck, TowTruckAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(CarType, CarTypeAdmin)
