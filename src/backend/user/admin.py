from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.safestring import SafeString, mark_safe

from core.models import EmptyFieldModel
from user.models import Avatar, User


@admin.register(User)
class UserAdmin(EmptyFieldModel):
    list_display = ("phone", "first_name", "last_name")
    list_filter = ("phone",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = (
        "phone",
        "first_name",
        "last_name",
    )
    ordering = ("phone",)

    def save_model(self, request, obj, form, change):
        """Хэширует пароль и сохраняет его в базе данных"""
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "preview")
    readonly_fields = ("preview",)
    list_per_page = 15
    list_max_show_all = 30

    def preview(self, obj: Avatar) -> SafeString:
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 300px;">'
            )
        return ""
