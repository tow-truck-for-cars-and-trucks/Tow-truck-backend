from django.db import models
from django.contrib import admin


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        # Это абстрактная модель:
        abstract = True


class EmptyFieldModel(admin.ModelAdmin):
    """
    Абстрактная модель. Добавляет красивое пустое поле.
    """
    empty_value_display = '-пусто-'

    class Meta:
        abstract = True


class MinValidatedInlineMixIn:
    """
    Производит валидацию Inline админ модели Django.
    Для прохождении валидации необходимо указать как минимум
    1 связанную запись с основной моделью.
    """
    validate_min = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(
            validate_min=self.validate_min, *args, **kwargs
        )
