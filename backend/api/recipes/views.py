from rest_framework import viewsets
from .serializers import TagSerializer
from recipes.models import TagsModel


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagsModel.objects.all()
    serializer_class = TagSerializer
