import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format_str, img_str = data.split(';base64,')
            ext = format_str.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
        return super().to_internal_value(data)
