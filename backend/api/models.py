from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """
    Теги рецептов.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Поле содержит недопустимые символы',
            ),
        ]
    )
    color = ColorField(
        unique=True,
        verbose_name='Цвет',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги для рецептов'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ингредиенты.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['id']

    def __str__(self):
        return self.name


class Follow(models.Model):
    """
    Подписки на авторов рецептов.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='На кого подписан пользователь'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    class Meta:
        verbose_name = 'подписку'
        verbose_name_plural = 'Подписки на авторов'

    def __str__(self):
        return f'{self.author}'


class Recipe(models.Model):
    """
    Рецепты.
    """
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientQuantity',
        related_name='recipe',
        verbose_name='Ингредиенты',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда'
    )
    text = models.TextField(
        verbose_name='Процесс приготовления',
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                'Минимальное время: 1 мин.'
            )
        ],
        verbose_name='Время приготовления, мин.',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты авторов'
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    """
    Количество ингредиента в рецепте.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='quantity',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(
            1,
            'Минимальный вес 1 гр.')
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Количество ингридиентов в рецептах'

    def __str__(self):
        return f'{self.ingredient}'


class Favorite(models.Model):
    """
    Избранные рецепты.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """
    Список покупок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Списки покупок в виде рецептов'

    def __str__(self):
        return f'{self.user}'
