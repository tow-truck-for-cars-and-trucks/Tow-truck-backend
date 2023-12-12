from django.contrib import admin

from core.models import MinValidatedInlineMixIn, EmptyFieldModel
from core.functions import avg_towtruck_score
from towin.models import Order, Feedback, TowTruck, Tariff, PriceOrder, CarType


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
    search_fields = (
        "address_from",
        "address_to",
    )
    readonly_fields = ("total_price",)
    inlines = [OrderriceTabularInline]

    def total_price(self, instance):
        return PriceOrder.objects.get(order=instance).total

    total_price.short_description = "Итоговая стоимость"


class FeedbackAdmin(EmptyFieldModel):
    list_display = ("order", "score", "comment")


class TowTruckAdmin(EmptyFieldModel):
    list_display = (
        "id",
        "is_active",
        "driver",
        "model_car",
        "license_plates",
        "avg_score",
    )

    def avg_score(self, instance):
        return avg_towtruck_score(instance)

    avg_score.short_description = "Средняя оценка"


class TariffAdmin(EmptyFieldModel):
    list_display = (
        "name",
        "description",
        "price",
        "delivery_time"
    )


class CarTypeAdmin(EmptyFieldModel):
    list_display = ("car_type", "price")


admin.site.register(Order, OdrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TowTruck, TowTruckAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(CarType, CarTypeAdmin)
