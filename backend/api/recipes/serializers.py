from rest_framework import serializers

from recipes.models import TagsModel

from recipes.models import IngredientsModel

from recipes.models import RecipesModel

from api.accounts.serializers import GetUserInfoSerializer
from recipes.models import RecipeIngredientModel
from api.serializers import Base64ImageField

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['id', 'name', 'slug']

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsModel
        fields = ['id', 'name', 'measurement_unit']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=IngredientsModel.objects.all(),
        source='ingredient'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientModel
        fields = ['id', 'name', 'measurement_unit', 'amount']

class GetRecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = GetUserInfoSerializer(read_only=True)
    image = Base64ImageField(read_only=True)

    ingredients = RecipeIngredientSerializer(
        many=True,
        source='ingredient_amount',
        read_only=True
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()


    class Meta:
        model = RecipesModel
        fields = ['id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  ]
    def get_is_favorited(self, obj):
        return False
    def get_is_in_shopping_cart(self, obj):
        return False
class CreateRecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='ingredient_amount',
        read_only=True
    )
    class Meta:
        model = RecipesModel
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
                  ]
    def to_representation(self, obj):
        request = self.context.get('request')
        return GetRecipesSerializer(
            obj,
            context={'request': request}
        ).data
    def create(self, validated_data):
        request = self.context.get('request')
        recipe = RecipesModel.objects.create(author=request.user, **validated_data)
        return recipe
