from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipesFilter
from .serializers import TagSerializer, IngredientsSerializer, GetRecipesSerializer, CreateRecipesSerializer, \
    ShoppingCartSerializer, FavoriteSerializer
from recipes.models import IngredientsModel, RecipesModel,TagsModel, ShoppingCartModel, FavoritesModel

from api.pagination import PageLimitPagination

from api.permissions import IsAuthorOrAdmin


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

    def get_serializer_class(self):
        if self.action == 'create' or 'update':
            return CreateRecipesSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthorOrAdmin()]
        return super().get_permissions()

    @action(methods=['post', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipesModel, id=pk)

        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={'user': user.id, 'recipe': recipe.id},
                                                context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            shopping_cart_item = ShoppingCartModel.objects.filter(user=user, recipe=recipe).first()
            if shopping_cart_item:
                shopping_cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Рецепт не найден в корзине"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipesModel, id=pk)

        if request.method == 'POST':
            serializer = FavoriteSerializer(data={'user': user.id, 'recipe': recipe.id}, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            favorite_item = FavoritesModel.objects.filter(user=user, recipe=recipe).first()
            if favorite_item:
                favorite_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Рецепт не найден в избранном"}, status=status.HTTP_400_BAD_REQUEST)
