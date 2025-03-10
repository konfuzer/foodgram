import django_filters

from recipes.models import IngredientsModel,RecipesModel


class IngredientsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = IngredientsModel
        fields = ['name']

class RecipesFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = RecipesModel
        fields = ['author', 'tags']
