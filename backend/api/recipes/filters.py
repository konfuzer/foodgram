from django_filters.rest_framework import FilterSet, filters

from recipes.models import IngredientsModel, RecipesModel


class IngredientsFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = IngredientsModel
        fields = ["name"]


class RecipesFilter(FilterSet):
    author = filters.NumberFilter(field_name="author__id", lookup_expr="exact")
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = filters.BooleanFilter(method="user_recipe_filter")
    is_in_shopping_cart = filters.BooleanFilter(method="user_recipe_filter")

    class Meta:
        model = RecipesModel
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def user_recipe_filter(self, queryset, name, value):

        user = self.request.user
        if not user.is_authenticated or not value:
            return queryset

        if name == "is_favorited":
            return queryset.filter(favoritesmodel__user=user)
        elif name == "is_in_shopping_cart":
            return queryset.filter(shoppingcartmodel__user=user)
        return queryset
