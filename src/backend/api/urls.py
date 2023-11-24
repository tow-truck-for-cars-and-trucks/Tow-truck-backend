from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api.views.towtruck import (
    OrderViewset,
    FeedbackViewset,
    TariffViewset,
    CarTypeViewset
)
from api.views.users import UserViewset

app_name = "api"

router = DefaultRouter()

router.register("user", UserViewset, basename="user")
router.register("order", OrderViewset, basename="order")
router.register("feedback", FeedbackViewset, basename="feedback")
router.register("tariff", TariffViewset, basename="tariff")
router.register("cartype", CarTypeViewset, basename="cartype")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
