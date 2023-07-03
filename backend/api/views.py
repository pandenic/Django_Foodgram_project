"""Describe custom views for the recipe app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, viewsets, status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.constants import HTTPMethods
from api.converters import convert_tuples_list_to_pdf
from api.errors import ErrorMessage
from api.filters import RecipeFilter, IngredientSearchFilter
from api.mixins import ListCreateRetrieveViewSet
from recipes.models import Tag, Recipe, Ingredient, Favorite, ShoppingCart
from api.pagination import LimitPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import TagSerializer, IngredientSerializer, GetRecipeSerializer, PostRecipeSerializer, \
    FavoriteRecipeSerializer, GetUserSerializer, SetPasswordSerializer, SubscriptionSerializer, PostUserSerializer, \
    GetTokenSerializer
from users.models import Follow

User = get_user_model()


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
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter
    http_method_names = [
        HTTPMethods.GET,
        HTTPMethods.POST,
        HTTPMethods.PATCH,
        HTTPMethods.DELETE,
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
        HTTPMethods.POST,
        HTTPMethods.DELETE,
    ], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        favorite_chain = Favorite.objects.filter(
            favorite_recipe=recipe,
            user=request.user,
        )
        if request.method == HTTPMethods.DELETE and favorite_chain:
            favorite_chain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST and favorite_chain:
            raise serializers.ValidationError({'errors': ErrorMessage.RECIPE_IN_FAVORITES})

        if request.method == HTTPMethods.DELETE:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        Favorite.objects.create(
            favorite_recipe=recipe,
            user=request.user,
        )
        return Response(FavoriteRecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    @action(methods=[
        HTTPMethods.POST,
        HTTPMethods.DELETE,
    ], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_in_shopping_cart = ShoppingCart.objects.filter(
            recipe_in_cart=recipe,
            user=request.user,
        )
        if request.method == HTTPMethods.DELETE and recipe_in_shopping_cart:
            recipe_in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST and recipe_in_shopping_cart:
            raise serializers.ValidationError({'errors': ErrorMessage.ALREADY_IN_SHOPPING_CART})

        if request.method == HTTPMethods.DELETE:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        ShoppingCart.objects.create(
            recipe_in_cart=recipe,
            user=request.user,
        )
        return Response(FavoriteRecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    @action(methods=[
        HTTPMethods.GET,
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


class UserViewSet(ListCreateRetrieveViewSet):
    """Perform GET and POST operations for User model."""

    queryset = User.objects.all()
    pagination_class = LimitPagination
    permission_classes = (permissions.AllowAny,)

    @action(
        (HTTPMethods.GET,),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Process './me' endpoint."""
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        (HTTPMethods.POST,),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        """Process './set_password' endpoint."""
        serializer = SetPasswordSerializer(
            request.user,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            password=make_password(
                serializer.validated_data['new_password']
            )
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        (HTTPMethods.GET,),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Process './subscriptions' endpoint."""
        subscriptions = User.objects.filter(followings__follower=request.user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request},
        )

        return self.get_paginated_response(serializer.data)

    @action(
        (HTTPMethods.POST, HTTPMethods.DELETE),
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk=None):
        """Process '.<id>/subscribe' endpoint."""
        user_to_follow = get_object_or_404(User, id=pk)
        follower_following_chain = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow,
        )

        if request.method == HTTPMethods.DELETE and follower_following_chain:
            follower_following_chain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST and follower_following_chain:
            raise serializers.ValidationError({'errors': ErrorMessage.ALREADY_SUBSCRIBED})

        if request.method == HTTPMethods.DELETE:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        if request.user == user_to_follow:
            raise serializers.ValidationError({'errors': ErrorMessage.CANNOT_FOLLOW_YOURSELF})

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow,
        )
        return Response(SubscriptionSerializer(user_to_follow).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Perform actions during save an instance of user."""
        serializer.save(
            password=make_password(serializer.validated_data['password']),
        )

    def get_serializer_class(self):
        """Choose serializer class depend on method."""
        if self.action in ('list', 'retrieve'):
            return GetUserSerializer
        return PostUserSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    """Obtain token for user."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    user = get_object_or_404(User, email=email)

    password = serializer.validated_data['password']
    if not check_password(password, user.password):
        return Response(
            {'password': 'Пароль неверный'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {'auth_token': token.key},
        status=status.HTTP_201_CREATED,
    )


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def delete_token(request):
    """Delete token for user."""
    token = get_object_or_404(Token, user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


