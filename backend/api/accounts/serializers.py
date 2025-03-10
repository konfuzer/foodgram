from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers

from api.serializers import Base64ImageField

UserModel = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['id'] = obj.id
        return data


class GetUserInfoSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'avatar', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return False



class UpdateUserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = UserModel
        fields = ('avatar',)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['avatar'] = obj.avatar.url if obj.avatar else None
        return data
