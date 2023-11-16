from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomUserViewset,
    OrderViewset,
    FeedbackViewset,
)

app_name = "api"

router = DefaultRouter()

router.register("user", CustomUserViewset, basename="user")
router.register("order", OrderViewset, basename="order")
router.register("feedback", FeedbackViewset, basename="feedback")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
