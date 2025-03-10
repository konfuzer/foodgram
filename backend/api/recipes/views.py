from rest_framework import viewsets
from .serializers import TagSerializer, IngredientsSerializer, RecipesSerializer
from recipes.models import TagsModel

from recipes.models import IngredientsModel,RecipesModel



class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagsModel.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientsModel.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecipesModel.objects.all()
    serializer_class = RecipesSerializer
