from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.accounts.serializers import GetUserInfoSerializer, CreateUserSerializer, UpdateUserAvatarSerializer, \
    CreateSubscriptionSerializer
from api.pagination import PageLimitPagination

from accounts.models import SubscriptionsModel

UserModel = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = GetUserInfoSerializer
    pagination_class = PageLimitPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action == 'me':
            return GetUserInfoSerializer
        return super().get_serializer_class()

    @action(methods=['put', 'delete'], detail=False, url_path='me/avatar')
    def me_avatar(self, request):
        user = request.user
        if request.method == 'PUT':
            serializer = UpdateUserAvatarSerializer(user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        subscribed_to = get_object_or_404(UserModel, id=id)

        if request.method == 'POST':
            serializer = CreateSubscriptionSerializer(data={
                'user': user.id,
                'subscribed_to': subscribed_to.id,
            },
                context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription = SubscriptionsModel.objects.filter(user=user, subscribed_to=subscribed_to).first()
            if subscription:
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Вы не подписаны"}, status=status.HTTP_400_BAD_REQUEST)
