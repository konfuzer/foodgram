from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    email = models.EmailField(
        "Адрес электронной почты", max_length=254, unique=True
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username + " " + self.email

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class SubscriptionsModel(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    subscribed_to = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscribers"
    )

    class Meta:
        unique_together = ("user", "subscribed_to")
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"{self.user} подписан на {self.subscribed_to}"
