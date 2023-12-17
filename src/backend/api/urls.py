from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

from api.views.towtruck import (
    OrderViewset,
    FeedbackViewset,
    TariffViewset,
    CarTypeViewset,
    TowTruckViewset,
)
from api.views.users import UserViewset

app_name = "api"

router = DefaultRouter()

router.register("user", UserViewset, basename="user")
router.register("order", OrderViewset, basename="order")
router.register("feedback", FeedbackViewset, basename="feedback")
router.register("tariff", TariffViewset, basename="tariff")
router.register("cartype", CarTypeViewset, basename="cartype")
router.register("towtruck", TowTruckViewset, basename="towtruck")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("auth/", include("djoser.urls")),
    re_path(r"auth/", include("djoser.urls.authtoken")),
    re_path(r"auth/", include("djoser.urls.jwt")),
]
