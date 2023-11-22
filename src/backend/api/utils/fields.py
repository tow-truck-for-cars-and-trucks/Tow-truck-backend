import base64

from django.core.files.base import ContentFile

# from django.shortcuts import get_object_or_404
from rest_framework import serializers


class LowercaseEmailField(serializers.EmailField):
    """
    Приводит email к нижнему регистру.
    """

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        return result.lower()


class Base64ImageField(serializers.ImageField):
    """
    Сохраняет изображение в base64.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)
