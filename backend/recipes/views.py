"""Describe custom views for the recipe app."""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.errors import Errors
from recipes.filters import RecipeFilter
from recipes.models import Tag, Recipe, Ingredient, Favorite
from recipes.pagination import RecipePagination
from recipes.serializers import TagSerializer, IngredientSerializer, GetRecipeSerializer, PostRecipeSerializer, \
    FavoriteRecipeSerializer


class HttpRequestMethods:

    GET_UPPER = 'GET'
    POST_UPPER = 'POST'
    DELETE_UPPER = 'DELETE'
    GET_LOWER = 'get'
    POST_LOWER = 'post'
    PATCH_LOWER = 'patch'
    DELETE_LOWER = 'delete'


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
    http_method_names = [
        HttpRequestMethods.GET_LOWER,
        HttpRequestMethods.POST_LOWER,
        HttpRequestMethods.PATCH_LOWER,
        HttpRequestMethods.DELETE_LOWER,
    ]

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

    @action(methods=[
        HttpRequestMethods.POST_LOWER,
        HttpRequestMethods.DELETE_LOWER,
    ], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        favorite_chain = Favorite.objects.filter(
            favorite_recipe=recipe,
            user=request.user,
        )
        if request.method == HttpRequestMethods.DELETE_UPPER and favorite_chain:
            favorite_chain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HttpRequestMethods.POST_UPPER and favorite_chain:
            raise serializers.ValidationError({'errors': Errors.RECIPE_IN_FAVORITES})

        if request.method == HttpRequestMethods.DELETE_UPPER:
            raise serializers.ValidationError({'errors': Errors.NOTHING_TO_DELETE})

        Favorite.objects.create(
            favorite_recipe=recipe,
            user=request.user,
        )
        return Response(FavoriteRecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    


