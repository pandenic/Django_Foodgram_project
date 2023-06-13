"""URL configuration for recipes app."""
from django.urls import path, include

from rest_framework import routers

from recipes.views import TagViewSet, IngredientViewSet

router = routers.SimpleRouter()
router.register(
    'tags',
    TagViewSet,
    basename='tags',
)
router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients',
)

urlpatterns = (
    path('', include(router.urls)),
)