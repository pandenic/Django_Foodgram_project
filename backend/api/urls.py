"""URL configuration for recipes app."""
from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UserViewSet, delete_token, get_token)

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
router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)
router.register('users', UserViewSet, basename='users')

token = [
    path('login/', get_token, name='token_obtain'),
    path('logout/', delete_token, name='token_deletion'),
]

urlpatterns = (
    path('', include(router.urls)),
    path('auth/token/', include(token)),
)
