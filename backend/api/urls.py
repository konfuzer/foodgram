from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.accounts.views import CustomUserViewSet

from api.recipes.views import TagViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
