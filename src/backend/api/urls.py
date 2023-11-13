from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewset,
    TowTruckViewset,
    TariffViewset,
    OrderViewset,
    PriceOrderViewset,
    FeedbackViewset,
)

app_name = "api"

router = DefaultRouter()

router.register("user", UserViewset, basename="user")
router.register("towtruck", TowTruckViewset, basename="towtruck")
router.register("tariff", TariffViewset, basename="tariff")
router.register("order", OrderViewset, basename="order")
router.register("priceorder", PriceOrderViewset, basename="priceorder")
router.register("feedback", FeedbackViewset, basename="feedback")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
