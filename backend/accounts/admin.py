from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    search_fields = ["username", "email"]
    list_display = ["username", "email", "avatar", "is_staff", "is_active"]
    ordering = ["-id"]


@admin.register(Subscription)
class SubscriptionsModelAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "subscribed_to__username"]
    list_display = ["user", "subscribed_to"]
