from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from api.accounts.serializers import GetUserInfoSerializer, CreateUserSerializer,UpdateUserAvatarSerializer

from api.pagination import PageLimitPagination


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