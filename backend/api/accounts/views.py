from django.db.models import Count
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import Subscription, User
from api.accounts.serializers import (
    CreateSubscriptionSerializer,
    CreateUserSerializer,
    GetSubscriptionUserInfoSerializer,
    GetUserInfoSerializer,
    UpdateUserAvatarSerializer,
)
from api.mixins import MultiSerializerViewSetMixin
from api.pagination import PageLimitPagination


class CustomUserViewSet(MultiSerializerViewSetMixin, UserViewSet):
    serializer_class = GetUserInfoSerializer
    pagination_class = PageLimitPagination
    serializer_classes = {
        "create": CreateUserSerializer,
        "me": GetUserInfoSerializer,
    }

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(methods=["put", "delete"], detail=False, url_path="me/avatar")
    def me_avatar(self, request):
        user = request.user
        if request.method == "PUT":
            serializer = UpdateUserAvatarSerializer(user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            user.avatar.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        if request.method == "POST":
            subscribed_to = get_object_or_404(
                User.objects.annotate(recipes_count=Count("recipes")), id=id
            )

            serializer = CreateSubscriptionSerializer(
                data={
                    "user": user.id,
                    "subscribed_to": subscribed_to.id,
                },
                context={"request": request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

        elif request.method == "DELETE":
            deleted_count, _ = Subscription.objects.filter(
                user=user, subscribed_to_id=id
            ).delete()

            if deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Вы не подписаны"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscribers__user=request.user
        ).annotate(recipes_count=Count("recipes"))
        result_pages = self.paginate_queryset(queryset=subscriptions)
        serializer = GetSubscriptionUserInfoSerializer(
            result_pages, context={"request": request}, many=True
        )
        return self.get_paginated_response(serializer.data)
