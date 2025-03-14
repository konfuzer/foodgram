from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    search_fields = ["username", "email", "first_name", "last_name"]
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "avatar",
        "is_staff",
        "is_active"
    ]
    ordering = ["-id"]


@admin.register(Subscription)
class SubscriptionsModelAdmin(admin.ModelAdmin):
    search_fields = [
        "user__username",
        "subscribed_to__username",
        "user__first_name",
        "user__last_name",
        "subscribed_to__first_name",
        "subscribed_to__last_name"
    ]
    list_display = ["user", "subscribed_to"]
