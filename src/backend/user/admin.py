from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.safestring import SafeString, mark_safe

from core.models import EmptyFieldModel
from user.models import Avatar

User = get_user_model()


@admin.register(User)
class UserAdmin(EmptyFieldModel):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
    )
    search_fields = (
        "phone",
        "first_name",
        "last_name",
        "email",
    )
    ordering = ("last_name", "first_name")
    list_per_page = 15
    list_max_show_all = 30

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
