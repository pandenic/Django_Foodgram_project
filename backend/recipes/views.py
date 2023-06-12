"""Describe custom views for the recipe app."""
from rest_framework import permissions, viewsets

from recipes.models import Tag, Recipe
from recipes.serializers import TagSerializer
from users.serializers import RecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Perform GET operations for Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Perform CRUD operations for Recipe model."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
