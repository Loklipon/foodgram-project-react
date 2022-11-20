from api.views import (DownloadShoppingCartAPIView, FavoriteAPIView,
                       FollowAPIView, IngredientView, RecipeView,
                       ShoppingCartAPIView, SubscriptionsView, TagView)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', TagView, basename='tags')
router.register('ingredients', IngredientView, basename='ingredients')
router.register('recipes', RecipeView, basename='recipies')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/subscriptions/', SubscriptionsView.as_view()),
    path('api/users/<int:id>/subscribe/', FollowAPIView.as_view()),
    path('api/', include('djoser.urls')),
    path('api/recipes/download_shopping_cart/',
         DownloadShoppingCartAPIView.as_view()),
    path('api/recipes/<int:id>/favorite/', FavoriteAPIView.as_view()),
    path('api/recipes/<int:id>/shopping_cart/', ShoppingCartAPIView.as_view()),
    path('api/', include(router.urls)),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
]
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
