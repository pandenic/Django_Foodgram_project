"""Describe custom views for the recipe app."""
from rest_framework import permissions, viewsets

from recipes.models import Tag, Recipe, Ingredient
from recipes.serializers import TagSerializer, IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Perform GET operations for Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Perform GET operations for Ingredients model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
