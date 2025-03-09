from rest_framework import viewsets
from .serializers import TagSerializer, IngredientsSerializer
from recipes.models import TagsModel

from recipes.models import IngredientsModel


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagsModel.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientsModel.objects.all()
    serializer_class = IngredientsSerializer
