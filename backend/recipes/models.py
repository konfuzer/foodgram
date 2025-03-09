from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TagsModel(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f"{self.title} {self.slug}"


class IngredientsModel(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    unit_of_measurement = models.CharField(
        max_length=30,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.title} {self.unit_of_measurement}"


class RecipesModel(models.Model):
    user_publishing = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации (пользователь)',
        related_name='recipes'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    picture = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )
    text_description = models.TextField(
        verbose_name='Текстовое описание'
    )

    ingredients = models.ManyToManyField(
        IngredientsModel,
        through='RecipeIngredientModel',
        verbose_name='Ингредиенты (продукты количество и ед. измерения)',
        related_name='in_recipes'
    )

    tags = models.ManyToManyField(
        TagsModel,
        verbose_name='Теги (множество)',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f"{self.title} {self.cooking_time} {self.user_publishing}"


class RecipeIngredientModel(models.Model):
    recipe = models.ForeignKey(
        RecipesModel,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amount'
    )
    ingredient = models.ForeignKey(
        IngredientsModel,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_amount'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количества ингредиента в рецепте'

    def __str__(self):
        return f'{self.recipe.title} {self.amount} {self.ingredient.title}'
