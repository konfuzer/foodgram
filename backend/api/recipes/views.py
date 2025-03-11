import base64

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import PageLimitPagination
from api.permissions import IsAuthorOrAdmin
from recipes.models import (
    FavoritesModel,
    IngredientsModel,
    RecipeIngredientModel,
    RecipesModel,
    ShoppingCartModel,
    TagsModel,
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
    queryset = TagsModel.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientsModel.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = RecipesModel.objects.all()
    serializer_class = GetRecipesSerializer
    pagination_class = PageLimitPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def retrieve(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            decoded_bytes = base64.urlsafe_b64decode(pk)
            pk = int(decoded_bytes.decode())
        except (ValueError, TypeError, base64.binascii.Error):
            return Response(
                {"detail": "Значение не подходит"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(RecipesModel, pk=pk)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create" or "update":
            return CreateRecipesSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthorOrAdmin()]
        return super().get_permissions()

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipesModel, id=pk)

        if request.method == "POST":
            serializer = ShoppingCartSerializer(
                data={"user": user.id, "recipe": recipe.id},
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

        elif request.method == "DELETE":
            shopping_cart_item = ShoppingCartModel.objects.filter(
                user=user, recipe=recipe
            ).first()
            if shopping_cart_item:
                shopping_cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Рецепт не найден в корзине"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipesModel, id=pk)

        if request.method == "POST":
            serializer = FavoriteSerializer(
                data={"user": user.id, "recipe": recipe.id},
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

        elif request.method == "DELETE":
            favorite_item = FavoritesModel.objects.filter(
                user=user, recipe=recipe
            ).first()
            if favorite_item:
                favorite_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Рецепт не найден в избранном"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredientModel.objects.filter(
                recipe__shoppingcartmodel__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("ingredient__name")
        )
        file_content = ""
        for item in ingredients:
            file_content += (
                f"{item['ingredient__name']} "
                f"{item['total_amount']}"
                f" {item['ingredient__measurement_unit']}\n"
            )
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
