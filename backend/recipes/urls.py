"""URL configuration for recipes app."""
from django.urls import path, include

from rest_framework import routers

from recipes.views import TagViewSet

router = routers.SimpleRouter()
router.register(
    'tags',
    TagViewSet,
    basename='tags',
)

urlpatterns = (
    path('', include(router.urls)),
)