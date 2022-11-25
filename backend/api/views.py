from http import HTTPStatus

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from api.serializers import (CreateUpdateRecipeSerializer,
                             FollowAndSubscriptionsSerializer,
                             IngredientSerializer, ShowRecipeSerializer,
                             ShowShortRecipeSerializer, TagSerializer)
from django.shortcuts import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            ShoppingCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow, User


class TagView(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для вывода тегов без пагинации.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientView(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для вывода ингредиентов;
    с фильтрацией, без пагинации.
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter
    pagination_class = None


class RecipeView(viewsets.ModelViewSet):
    """
    Вьюсет для отображения, создания,
    частичного изменения, удаления рецептов;
    с фильтрацией и пагинацией;
    с разными правами доступа.
    """
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (IsAuthorOrIsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateRecipeSerializer
        return ShowRecipeSerializer


class FavoriteAPIView(APIView):
    """
    Вью-класс для создания и удаления подписок;
    для авторизованных пользователей.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Этот рецепт уже был добавлен в избранное'},
                status=HTTPStatus.BAD_REQUEST
            )
        Favorite.objects.create(
            user=user,
            recipe=recipe
        )
        return Response(
            ShowShortRecipeSerializer(recipe).data,
            status=HTTPStatus.CREATED
        )

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if not Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Такого рецепта нет в избранном'},
                status=HTTPStatus.BAD_REQUEST
            )
        Favorite.objects.get(
            user=user,
            recipe=recipe
        ).delete()
        return Response(
            status=HTTPStatus.NO_CONTENT
        )


class ShoppingCartAPIView(APIView):
    """
    Вью-класс для измнения списка покупок (добавление, удаление);
    для авторизованных пользователей.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Этот рецепт уже есть в списке покупок'},
                status=HTTPStatus.BAD_REQUEST
            )
        ShoppingCart.objects.create(
            user=user,
            recipe=recipe
        )
        return Response(
            ShowShortRecipeSerializer(recipe).data,
            status=HTTPStatus.CREATED
        )

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if not ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Такого рецепта нет в списке покупок'},
                status=HTTPStatus.NO_CONTENT
            )
        ShoppingCart.objects.get(
            user=user,
            recipe=recipe
        ).delete()
        return Response(
            status=HTTPStatus.NO_CONTENT
        )


class DownloadShoppingCartAPIView(APIView):
    """
    Вью-класс для формирования и скачивания списка покупок;
    для авторизованных пользователей.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        grocery_list = IngredientQuantity.objects.filter(
            recipe__shopping_carts__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        final_grocery_list = {}
        for item in grocery_list:
            name = item[0]
            if name not in final_grocery_list:
                final_grocery_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_grocery_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(TTFont('Arial', 'data/arial.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'
        page = canvas.Canvas(response)
        page.setFont('Arial', 14)
        page.drawString(250, 800, 'Список покупок:')
        page.setFont('Arial', 14)
        height = 750
        for i, (name, data) in enumerate(final_grocery_list.items(), 1):
            page.drawString(
                75, height, (f'{i}) {name.capitalize()} - {data["amount"]} '
                             f'{data["measurement_unit"]}.')
            )
            height -= 25
        page.showPage()
        page.save()
        return response


class SubscriptionsView(ListAPIView):
    """
    Вью-класс для отображения подписок;
    для авторизованных пользователей.
    """
    serializer_class = FollowAndSubscriptionsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(
            subscriptions__user=self.request.user
        )


class FollowAPIView(APIView):
    """
    Вью-класс для создания и удаленя подписок;
    для авторизованных пользователей.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if Follow.objects.filter(
            author=id,
            user=request.user
        ).exists():
            return Response(
                {'errors': 'Такая подписка уже существует'},
                status=HTTPStatus.BAD_REQUEST
            )
        if request.user == author:
            return Response(
                {'errors': 'Нельзя подписаться на себя'},
                status=HTTPStatus.BAD_REQUEST
            )
        Follow.objects.create(
            user=request.user,
            author_id=id
        )
        return Response(
            FollowAndSubscriptionsSerializer(author, context={'request': request}).data,
            status=HTTPStatus.CREATED
        )

    def delete(self, request, id):
        get_object_or_404(User, id=id)
        if not Follow.objects.filter(
            author=id,
            user=request.user
        ).exists():
            return Response(
                {'errors': 'Такой подписки не существует'},
                status=HTTPStatus.BAD_REQUEST
            )
        Follow.objects.get(
            author=id,
            user=request.user
        ).delete()
        return Response(
            status=HTTPStatus.NO_CONTENT
        )
