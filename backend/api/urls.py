from api.views import (DownloadShoppingCartAPIView, FavoriteAPIView,
                       FollowAPIView, IngredientView, RecipeView,
                       ShoppingCartAPIView, SubscriptionsView, TagView)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', TagView, basename='tags')
router.register('ingredients', IngredientView, basename='ingredients')
router.register('recipes', RecipeView, basename='recipies')
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('users/<int:id>/subscribe/', FollowAPIView.as_view()),
    path('', include('djoser.urls')),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartAPIView.as_view()),
    path('recipes/<int:id>/favorite/', FavoriteAPIView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartAPIView.as_view()),
    path('', include(router.urls)),
]
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
