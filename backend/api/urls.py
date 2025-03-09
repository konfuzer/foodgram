from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.accounts.views import CustomUserViewSet


from api.recipes.views import IngredientsViewSet, TagsViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
