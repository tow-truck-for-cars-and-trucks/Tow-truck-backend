from django.contrib import admin

from .models import (
    Order,
    Feedback,
    TowTruck,
    Tariff,
    PriceInOrder,
    CarType,
    Price,
)


# class CarTypeInPriceInline(admin.StackedInline):
#     model = CarTypeInPrice
#     extra = 0


# class TariffInPriceInline(admin.StackedInline):
#     model = TariffInPrice
#     extra = 0


class PriceInOrderInline(admin.StackedInline):
    model = PriceInOrder
    extra = 0


@admin.register(Order)
class OdrderAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "address_from",
        "address_to",
        "created",
        "addition",
        "delay",
        "tow_truck",
    )
    empty_value_display = "--пусто--"
    inlines = (PriceInOrderInline,)


@admin.register(TowTruck)
class TowTruckAdmin(admin.ModelAdmin):
    list_display = ("is_active", "driver")
    empty_value_display = "--пусто--"


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ("car_type", "car_type_price")
    empty_value_display = "--пусто--"


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("name", "tariff_price")
    empty_value_display = "--пусто--"


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("tariff", "car_type", "wheel_lock", "towin")
    empty_value_display = "--пусто--"
    # inlines = (
    #     CarTypeInPrice,
    #     TariffInPrice,
    # )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "score",
        "comment",
        "order",
    )
    empty_value_display = "--пусто--"


# admin.site.register(Order, OdrderAdmin)
# admin.site.register(Feedback, FeedbackAdmin)
# admin.site.register(TowTruck, TowTruckAdmin)
# admin.site.register(Tariff, TariffAdmin)
