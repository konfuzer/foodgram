from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ["ingredient", "amount"]
    autocomplete_fields = ["ingredient"]


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(Ingredient)
class IngredientsModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Recipe)
class RecipeModelAdmin(admin.ModelAdmin):
    search_fields = ["name", "author__username"]
    list_filter = ["tags"]
    readonly_fields = ["get_favorites_count"]
    inlines = [RecipeIngredientInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("author").prefetch_related("ingredients", "tags")

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = "Избранное"


@admin.register(RecipeIngredient)
class RecipeIngredientModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ingredient", "amount"]


@admin.register(Favorite)
class FavoriteModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe__name", "user__username"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("recipe", "user")


@admin.register(ShoppingCart)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe__name", "user__username"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("recipe", "user")
