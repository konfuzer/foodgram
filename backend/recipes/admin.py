from django.contrib import admin
from .models import (
    TagsModel,
    IngredientsModel,
    RecipesModel,
    RecipeIngredientModel,
    FavoritesModel,
    ShoppingCartModel,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredientModel
    extra = 1
    fields = ["ingredient", "amount"]
    autocomplete_fields = ["ingredient"]


@admin.register(TagsModel)
class TagsModelAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]


@admin.register(IngredientsModel)
class IngredientsModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(RecipesModel)
class RecipesModelAdmin(admin.ModelAdmin):
    search_fields = ["name", "author__username"]
    list_filter = ["tags"]
    readonly_fields = ["get_favorites_count"]
    inlines = [RecipeIngredientInline]

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = "Избранное"


@admin.register(RecipeIngredientModel)
class RecipeIngredientModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ingredient", "amount"]


@admin.register(FavoritesModel)
class FavoritesModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe__name", "user__username"]


@admin.register(ShoppingCartModel)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe__name", "user__username"]
