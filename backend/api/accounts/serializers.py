from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from accounts.models import Subscription, User
from api.serializers import Base64ImageField


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["id"] = obj.id
        return data


class GetUserInfoSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        return False


class UpdateUserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ("avatar",)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["avatar"] = obj.avatar.url if obj.avatar else None
        return data


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "subscribed_to")

    def validate(self, data):
        user = self.context["request"].user
        target_user = data.get("subscribed_to")
        if user == target_user:
            raise serializers.ValidationError(
                {"error": "Нельзя подписаться на себя"}
            )
        return data

    def to_representation(self, obj):
        request = self.context.get("request")
        return GetSubscriptionUserInfoSerializer(
            obj.subscribed_to, context={"request": request}
        ).data


class GetSubscriptionUserInfoSerializer(GetUserInfoSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True, default=0)

    class Meta(GetUserInfoSerializer.Meta):
        model = User
        fields = GetUserInfoSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        from api.recipes.serializers import GetMiniRecipesSerializer

        request = self.context.get("request")
        recipes_limit = request.query_params.get("recipes_limit")

        if isinstance(recipes_limit, str) and not recipes_limit.isdigit():
            recipes_limit = None

        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]

        return GetMiniRecipesSerializer(
            recipes, many=True, context=self.context
        ).data
