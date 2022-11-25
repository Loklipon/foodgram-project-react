from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'add_to_favorite')
    list_filter = ('tags',)
    search_fields = ('author', 'name')

    def has_add_permission(self, request, obj=None):
        return False

    def add_to_favorite(self, obj):
        return obj.favorites.count()

    add_to_favorite.short_description = 'Добавлено в избранное'


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')

    def has_add_permission(self, request, obj=None):
        return False
