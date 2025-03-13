from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Адрес электронной почты", max_length=254, unique=True
    )
    username = models.CharField(
        max_length=150,
        verbose_name="Уникальный юзернейм",
        unique=True,
        validators=[validate_username],
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} {self.email}"

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Подписчик пользователя",
    )

    class Meta:
        unique_together = ("user", "subscribed_to")
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"{self.user} подписан на {self.subscribed_to}"
