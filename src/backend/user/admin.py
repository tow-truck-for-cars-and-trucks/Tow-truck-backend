from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_editable = ('role',)
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        """Хэширует пароль и сохраняет его в базе данных"""
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)