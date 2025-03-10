from rest_framework import viewsets
from .serializers import TagSerializer, IngredientsSerializer, GetRecipesSerializer,CreateRecipesSerializer
from recipes.models import TagsModel
from recipes.models import IngredientsModel,RecipesModel

from api.pagination import PageLimitPagination


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
        if self.action == 'create':
            return CreateRecipesSerializer
        return super().get_serializer_class()
