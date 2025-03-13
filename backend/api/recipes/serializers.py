from rest_framework import serializers

from api.accounts.serializers import GetUserInfoSerializer
from api.serializers import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient"
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class GetMiniRecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]


class GetRecipesSerializer(GetMiniRecipesSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = GetUserInfoSerializer(read_only=True)

    ingredients = RecipeIngredientSerializer(
        many=True, source="ingredient_amount", read_only=True
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta(GetMiniRecipesSerializer.Meta):
        model = Recipe
        fields = GetMiniRecipesSerializer.Meta.fields + [
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "text",
        ]

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.shopping_carts.filter(user=user).exists()
        return False


class CreateRecipesSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = [
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        ]

    def to_representation(self, obj):
        request = self.context.get("request")
        return GetRecipesSerializer(obj, context={"request": request}).data

    def update_ingredients_tags(self, recipe, ingredients_data, tags_data):
        recipe.ingredient_amount.all().delete()
        recipe.tags.clear()
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=data["ingredient"],
                amount=data["amount"],
            )
            for data in ingredients_data
        ]

        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        recipe.tags.set(tags_data)

    def create(self, validated_data):
        request = self.context.get("request")
        ingredients_data = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        self.update_ingredients_tags(recipe, ingredients_data, tags_data)
        return recipe

    def update(self, obj, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])
        super().update(obj, validated_data)
        self.update_ingredients_tags(obj, ingredients_data, tags_data)
        return obj

    def validate(self, data):

        tags = data.get("tags", [])
        if not tags:
            raise serializers.ValidationError({"tags": "Теги обязательны"})
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                {"tags": "Теги не должны повторяться"}
            )

        ingredients = data.get("ingredients", [])
        if not ingredients:
            raise serializers.ValidationError(
                {"ingredients": "Ингредиенты обязательны"}
            )
        ingredient_ids = [
            ingredient.get("ingredient").id for ingredient in ingredients
        ]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {"ingredients": "Ингредиенты не должны повторяться"}
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ["user", "recipe"]

    def validate(self, data):
        user = data["user"]
        recipe = data["recipe"]
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Этот рецепт уже в корзине покупок"
            )
        return data

    def to_representation(self, obj):
        request = self.context.get("request")
        return GetMiniRecipesSerializer(
            obj.recipe, context={"request": request}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["user", "recipe"]

    def validate(self, data):
        user = data["user"]
        recipe = data["recipe"]
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("Этот рецепт уже в избранном")
        return data

    def to_representation(self, obj):
        request = self.context.get("request")
        return GetMiniRecipesSerializer(
            obj.recipe, context={"request": request}
        ).data
