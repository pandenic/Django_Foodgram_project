"""Describe custom views for the recipe app."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import Tag, Recipe, Ingredient
from recipes.pagination import RecipePagination
from recipes.serializers import TagSerializer, IngredientSerializer, GetRecipeSerializer, PostRecipeSerializer


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Perform CRUD operations for Recipe model."""

    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        """Perform actions during save an instance of user."""
        serializer.save(
            author=self.request.user,
        )

    def get_serializer_class(self):
        """Choose serializer class depend on method."""
        if self.action in ('list', 'retrieve'):
            return GetRecipeSerializer
        return PostRecipeSerializer
