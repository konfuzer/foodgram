from rest_framework import serializers

from recipes.models import TagsModel

from recipes.models import IngredientsModel

from recipes.models import RecipesModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['id', 'name', 'slug']

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsModel
        fields = ['id', 'name', 'measurement_unit']

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipesModel