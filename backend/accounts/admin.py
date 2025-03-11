from django.contrib.auth import get_user_model
from django.contrib import admin

from .models import SubscriptionsModel
from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    search_fields = ["username", "email"]
    list_display = ["username", "email", "avatar", "is_staff", "is_active"]
    ordering = ["-id"]


@admin.register(SubscriptionsModel)
class SubscriptionsModelAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "subscribed_to__username"]
    list_display = ["user", "subscribed_to"]
