from django.contrib import admin
from core.models import EmptyFieldModel
from .models import Order, Feedback, TowTruck, Tariff, Price


class OdrderAdmin(EmptyFieldModel):
    list_display = ('client', 'address_from', 'address_to', 'created',
                    'price', 'addition', 'delay', 'tow_truck')


class FeedbackAdmin(EmptyFieldModel):
    list_display = ('score', 'comment', 'order')


class TowTruckAdmin(EmptyFieldModel):
    list_display = ('is_active', 'driver')


class TariffAdmin(EmptyFieldModel):
    list_display = ('name', 'description', 'price')


class PriceAdmin(EmptyFieldModel):
    list_display = ('tariff', 'car_type', 'wheel_lock', 'towin')


admin.site.register(Order, OdrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TowTruck, TowTruckAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(Price, PriceAdmin)
