from rest_framework import serializers

from recipes.models import TagsModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['id', 'name', 'slug']
