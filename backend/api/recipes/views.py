from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializer, IngredientsSerializer, GetRecipesSerializer,CreateRecipesSerializer
from recipes.models import TagsModel
from recipes.models import IngredientsModel,RecipesModel

from api.pagination import PageLimitPagination

from ..permissions import IsAuthorOrAdmin


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagsModel.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientsModel.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = RecipesModel.objects.all()
    serializer_class = GetRecipesSerializer
    pagination_class = PageLimitPagination

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
