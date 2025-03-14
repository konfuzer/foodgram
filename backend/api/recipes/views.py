import base64

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from api.mixins import MultiSerializerViewSetMixin
from api.pagination import PageLimitPagination
from api.permissions import IsAuthorOrAdmin
from api.utils import convert_base64_int, create_output_shopping_cart
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)

from .filters import IngredientsFilter, RecipesFilter
from .serializers import (
    CreateRecipesSerializer,
    FavoriteSerializer,
    GetRecipesSerializer,
    IngredientsSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class RecipesViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("author").prefetch_related(
        "tags",
        "ingredients",
    )
    serializer_class = GetRecipesSerializer
    pagination_class = PageLimitPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter
    serializer_classes = {
        "create": CreateRecipesSerializer,
        "partial_update": CreateRecipesSerializer,
    }

    def get_object(self):
        self.kwargs["pk"] = convert_base64_int(self.kwargs["pk"])
        return super().get_object()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthorOrAdmin()]
        return super().get_permissions()

    def handle_favorite_or_cart(
        self, request, pk, model, serializer_class, error_message
    ):
        user = request.user

        if request.method == "POST":
            recipe = get_object_or_404(Recipe, id=pk)
            serializer = serializer_class(
                data={"user": user.id, "recipe": recipe.id},
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        elif request.method == "DELETE":
            deleted_count, _ = model.objects.filter(
                user=user, recipe_id=pk).delete()
            if deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": error_message},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return self.handle_favorite_or_cart(
            request,
            pk,
            ShoppingCart,
            ShoppingCartSerializer,
            "Рецепт не найден в корзине",
        )

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self.handle_favorite_or_cart(
            request,
            pk,
            Favorite,
            FavoriteSerializer,
            "Рецепт не найден в избранном",
        )

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_carts__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("ingredient__name")
        )
        file_content = create_output_shopping_cart(ingredients)
        response = HttpResponse(file_content, content_type="text/plain")
        response["Content-Disposition"] = (
            "attachment;" ' filename="shopping_cart.txt"'
        )
        return response

    @action(methods=["get"], detail=True, url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        encoded_id = base64.urlsafe_b64encode(str(recipe.id).encode()).decode()
        host = request.META["HTTP_HOST"]
        return Response(
            {"short-link": f"{host}/s/{encoded_id}/"},
            status=status.HTTP_200_OK,
        )
