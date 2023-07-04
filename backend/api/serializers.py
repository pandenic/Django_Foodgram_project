"""Describe custom serializers for an Api app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.converters import Base64ImageField
from api.errors import ErrorMessage
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Follow

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Serialize requests for Tag model."""

    class Meta:
        """Describe settings for TagSerializer."""

        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize requests for Ingredients model."""

    amount = serializers.SerializerMethodField()

    class Meta:
        """Describe settings for IngredientSerializer."""

        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_amount(self, obj):
        """Retrieve ingredient amount from IngredientRecipe model."""
        if 'current_recipe_id' not in self.context:
            return None
        ingredient_recipe = IngredientRecipe.objects.get(
            ingredient=obj.id,
            recipe=self.context['current_recipe_id'],
        )
        return ingredient_recipe.quantity


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serialize requests for IngredientRecipe model."""

    id = serializers.IntegerField(read_only=False)
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        """Describe settings for IngredientRecipeSerializer."""

        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, value):
        """Check if amount greater than or equal to 0."""
        if value <= 0 or value is None:
            raise serializers.ValidationError(
                {'amount': ErrorMessage.WRONG_INGREDIENTS_AMOUNT}
            )
        return value

    def validate_id(self, value):
        """Check if ingredient with exact id exists."""
        get_object_or_404(Ingredient, id=value)
        return value


class GetUserSerializer(serializers.ModelSerializer):
    """Serialize GET request for a User model."""

    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254,
    )

    class Meta:
        """Describe settings for GetUserSerializer."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Check if current user follow exact user."""
        request = self.context.get('request')
        if request:
            return (
                Follow.objects.filter(
                    follower=request.user.id,
                )
                .filter(
                    following=obj.id,
                )
                .exists()
            )
        return False


class GetRecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for a Recipe model."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    author = GetUserSerializer(read_only=True)
    text = serializers.CharField(source='description')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Check if current recipe is in favorite of a user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return (
                Favorite.objects.filter(
                    user=request.user,
                )
                .filter(
                    favorite_recipe=obj.id,
                )
                .exists()
            )
        return False

    def get_is_in_shopping_cart(self, obj):
        """Check if current recipe is in shopping cart of a user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return (
                ShoppingCart.objects.filter(
                    user=request.user,
                )
                .filter(
                    recipe_in_cart=obj.id,
                )
                .exists()
            )
        return False

    def get_ingredients(self, obj):
        """Retrive ingredients from an Ingredient model."""
        return IngredientSerializer(
            obj.ingredients.all(),
            many=True,
            context={'current_recipe_id': obj.id},
        ).data


class PostRecipeSerializer(serializers.ModelSerializer):
    """Serialize POST request for Recipe model."""

    tags = serializers.PrimaryKeyRelatedField(
        read_only=False, required=True, many=True, queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(
        many=True, required=True, source='ingredient_recipe'
    )
    text = serializers.CharField(source='description')
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        """Describe settings for PostRecipeSerializer."""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def add_ingredients(self, recipe, ingredients):
        """Add ingredient - recipe chains if they do not exist."""
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                ingredient_id=ingredient['id'],
                recipe=recipe,
                quantity=ingredient['quantity'],
            )

    def create(self, validated_data):
        """Define a way how Recipe instance is creating."""
        ingredients = validated_data.pop('ingredient_recipe')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        self.add_ingredients(
            recipe=recipe,
            ingredients=ingredients,
        )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        """Define a way how Recipe instance is updating."""
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        ingredients = validated_data.pop('ingredient_recipe')
        tags = validated_data.pop('tags')

        instance.ingredients.clear()
        self.add_ingredients(
            recipe=instance,
            ingredients=ingredients,
        )
        instance.tags.set(tags)
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Serialize requests for FavoriteRecipe model."""

    class Meta:
        """Describe settings for FavoriteRecipeSerializer."""

        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class PostUserSerializer(serializers.ModelSerializer):
    """Serialize POST request for a User model."""

    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254,
    )

    class Meta:
        """Describe settings for PostUserSerializer."""

        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def to_representation(self, data):
        """Define representation of PostUserSerializer."""
        return {
            'email': data.email,
            'id': data.id,
            'username': data.username,
            'first_name': data.first_name,
            'last_name': data.last_name,
        }

    def validate(self, attrs):
        """Check if all required fields are filled."""
        for attr, value in attrs.items():
            if not value:
                raise serializers.ValidationError({attr: 'Обязательное поле.'})
        return attrs


class SetPasswordSerializer(serializers.ModelSerializer):
    """Serialize a set password request."""

    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(
        source='password',
        max_length=150,
    )

    class Meta:
        """Describe settings for SetPasswordSerializer."""

        model = User
        fields = (
            'new_password',
            'current_password',
        )

    def validate_current_password(self, value):
        """Check if current password is correct."""
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError(
                {'current_password': 'Пароль неверный'}
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Serialize GET request for token obtaining."""

    password = serializers.CharField(max_length=150)
    email = serializers.EmailField()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serialize requests for Subscription model."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Describe settings for SubscriptionSerializer."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        """Check if current user follows exact user."""
        request = self.context.get('request')
        if not request:
            return False
        return Follow.objects.filter(
            follower=request.user,
            following=obj,
        ).exists()

    def get_recipes(self, obj):
        """Gather all recipes from favorites."""
        request = self.context.get('request')
        if not request:
            return None
        limit = request.query_params.get('recipes_limit')
        limit = int(limit) if limit and limit.isdigit() else 1
        serializer = FavoriteRecipeSerializer(
            Recipe.objects.filter(author=obj)[:limit],
            many=True,
        )
        return serializer.data

    def get_recipes_count(self, obj):
        """Count user's recipes amount."""
        return Recipe.objects.filter(
            author=obj,
        ).count()
