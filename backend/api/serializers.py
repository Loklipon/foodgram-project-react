import base64

from api.models import (Favorite, Follow, Ingredient, IngredientQuantity,
                        Recipe, ShoppingCart, Tag, User)
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import ShowUserSerializer


class ShowShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения рецептов
    в подписках.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowAndSubscriptionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения подписок.
    """
    recipes = serializers.SerializerMethodField(
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        elif Follow.objects.filter(
            user=user,
            author=obj
        ).exists():
            return True
        else:
            return False

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)[:3]
        return ShowShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения тегов.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ингредиентов.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientQuantityWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записи количества ингредиента в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'amount')


class IngredientQuantityShowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ингредиентов в рецепте.
    """
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ShowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов.
    """
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    tags = TagSerializer(
        many=True
    )
    author = ShowUserSerializer(
        read_only=True
    )
    ingredients = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        queryset = IngredientQuantity.objects.filter(recipe=obj)
        return IngredientQuantityShowSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        elif Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists():
            return True
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        elif ShoppingCart.objects.filter(
            user=user,
            recipe=obj
        ).exists():
            return True
        else:
            return False


class Base64ImageField(serializers.ImageField):
    """
    Сериализатор для декодирования изображений.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления рецепта.
    """
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    ingredients = IngredientQuantityWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('tags', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        IngredientQuantity.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = instance
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeSerializer(instance, context=context).data
