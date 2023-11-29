from django.contrib import admin
from core.models import MinValidatedInlineMixIn
from core.models import EmptyFieldModel
from .models import Order, Feedback, TowTruck, Tariff, PriceOrder, CarType


class OrderriceTabularInline(admin.TabularInline, MinValidatedInlineMixIn):
    model = PriceOrder
    validate_min = True
    min_num = 1


class OdrderAdmin(EmptyFieldModel):
    list_display = (
        "client",
        "address_from",
        "address_to",
        "created",
        "addition",
        "delay",
        "tow_truck",
    )
<<<<<<< HEAD
    inlines = [OrderriceTabularInline]

=======
    search_fields = (
        "address_from",
        "address_to",
    )
    readonly_fields = ("total_price",)
    inlines = [OrderriceTabularInline]

    def total_price(self, instance):
        return PriceOrder.objects.get(order=instance).total

    total_price.short_description = "Итоговая стоимость"

>>>>>>> develop

class FeedbackAdmin(EmptyFieldModel):
    list_display = ("score", "comment", "order")


class TowTruckAdmin(EmptyFieldModel):
<<<<<<< HEAD
    list_display = ("is_active", "driver")
=======
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
>>>>>>> develop


class TariffAdmin(EmptyFieldModel):
    list_display = ("name", "description", "price")


class CarTypeAdmin(EmptyFieldModel):
    list_display = ("car_type", "car_type_price")


admin.site.register(Order, OdrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TowTruck, TowTruckAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(CarType, CarTypeAdmin)
