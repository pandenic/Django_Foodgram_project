"""Describe custom views for the recipe app."""
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from foodgram.constants import HTTPMethods
from recipes.converters import convert_tuples_list_to_pdf
from recipes.errors import ErrorMessage
from recipes.filters import RecipeFilter, IngredientSearchFilter
from recipes.models import Tag, Recipe, Ingredient, Favorite, ShoppingCart
from recipes.pagination import RecipePagination
from recipes.permissions import AuthorOrReadOnly
from recipes.serializers import TagSerializer, IngredientSerializer, GetRecipeSerializer, PostRecipeSerializer, \
    FavoriteRecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Perform GET operations for Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Perform GET operations for Ingredients model."""

    queryset = Ingredient.objects.all()
    filter_backends = (IngredientSearchFilter,)
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Perform CRUD operations for Recipe model."""

    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter
    http_method_names = [
        HTTPMethods.GET_LOWER,
        HTTPMethods.POST_LOWER,
        HTTPMethods.PATCH_LOWER,
        HTTPMethods.DELETE_LOWER,
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
        HTTPMethods.POST_LOWER,
        HTTPMethods.DELETE_LOWER,
    ], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        favorite_chain = Favorite.objects.filter(
            favorite_recipe=recipe,
            user=request.user,
        )
        if request.method == HTTPMethods.DELETE_UPPER and favorite_chain:
            favorite_chain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST_UPPER and favorite_chain:
            raise serializers.ValidationError({'errors': ErrorMessage.RECIPE_IN_FAVORITES})

        if request.method == HTTPMethods.DELETE_UPPER:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        Favorite.objects.create(
            favorite_recipe=recipe,
            user=request.user,
        )
        return Response(FavoriteRecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    @action(methods=[
        HTTPMethods.POST_LOWER,
        HTTPMethods.DELETE_LOWER,
    ], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_in_shopping_cart = ShoppingCart.objects.filter(
            recipe_in_cart=recipe,
            user=request.user,
        )
        if request.method == HTTPMethods.DELETE_UPPER and recipe_in_shopping_cart:
            recipe_in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST_UPPER and recipe_in_shopping_cart:
            raise serializers.ValidationError({'errors': ErrorMessage.ALREADY_IN_SHOPPING_CART})

        if request.method == HTTPMethods.DELETE_UPPER:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        ShoppingCart.objects.create(
            recipe_in_cart=recipe,
            user=request.user,
        )
        return Response(FavoriteRecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    @action(methods=[
        HTTPMethods.GET_LOWER,
    ], detail=False)
    def download_shopping_cart(self, request):
        ingredients = Ingredient.objects.filter(
            recipes__recipe__added_to_cart__user=request.user,
        ).annotate(
            amount=Sum('recipes__recipe__ingredient_recipe__quantity'),
        )
        ingredients = ingredients.values_list('name', 'amount', 'measurement_unit')
        pdf_ingredients = convert_tuples_list_to_pdf(ingredients, 'Ingredients')
        return FileResponse(pdf_ingredients, as_attachment=True, filename="shopping_cart.pdf")


