"""URL configuration for recipes app."""
from django.urls import path, include

from rest_framework import routers

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet, UserViewSet, get_token, delete_token

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
router.register(
    'users',
    UserViewSet,
    basename='users'
)

token = [
    path('login/', get_token, name='token_obtain'),
    path('logout/', delete_token, name='token_deletion'),
]

urlpatterns = (
    path('', include(router.urls)),
    path('auth/token/', include(token))
)