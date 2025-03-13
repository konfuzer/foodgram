from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name} {self.slug}"


class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=30, verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} {self.measurement_unit}"


class Recipe(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации (пользователь)",
        related_name="recipes",
    )
    name = models.CharField(max_length=256, verbose_name="Название")
    image = models.ImageField(upload_to="recipes/", verbose_name="Картинка")
    text = models.TextField(verbose_name="Текстовое описание")

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты (продукты количество и ед. измерения)",
        related_name="recipes",
    )

    tags = models.ManyToManyField(
        Tag, verbose_name="Теги (множество)", related_name="recipes"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления в минутах",
        validators=[MinValueValidator(1), MaxValueValidator(600)],
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-publish_date"]

    def __str__(self):
        return f"{self.name} {self.cooking_time} {self.author}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="ingredient_amount",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="recipe_amount",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1), MaxValueValidator(500)],
    )

    class Meta:
        verbose_name = "Количество ингредиента в рецепте"
        verbose_name_plural = "Количества ингредиента в рецепте"

    def __str__(self):
        return f"{self.recipe.name} {self.amount} {self.ingredient.name}"


class UserRecipeRelation(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.recipe} - {self.user}"


class Favorite(UserRecipeRelation):
    class Meta(UserRecipeRelation.Meta):
        verbose_name = "Избранное у пользователя"
        verbose_name_plural = "Избранные у пользователей"
        default_related_name = "favorites"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite_recipe"
            ),
        ]

    def __str__(self):
        return f"{self.recipe.name} в избранном у {self.user.username}"


class ShoppingCart(UserRecipeRelation):
    class Meta(UserRecipeRelation.Meta):
        verbose_name = "Корзина покупок у пользователя"
        verbose_name_plural = "Корзины покупок у пользователей"
        default_related_name = "shopping_carts"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            ),
        ]

    def __str__(self):
        return f"{self.recipe.name} в корзине у {self.user.username}"
