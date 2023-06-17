"""Describe custom serializers for the recipes app."""
import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, TagRecipe, IngredientRecipe
from users.serializers import GetUserSerializer


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

    class Meta:
        """Describe settings for IngredientSerializer."""

        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = ('name',)


class IngredientRecipeSerializer(serializers.Serializer):
    """Serialize requests for IngredientsRecipe model."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate(self, attrs):
        return attrs


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GetRecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for Recipe model."""

    ingredients = IngredientRecipeSerializer(many=True)
    author = GetUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    text = serializers.CharField(source='description')

    class Meta:
        """Describe settings for RecipeSerializer."""

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
        if request:
            return Favorite.objects.filter(
                user=request.user,
            ).filter(
                favorite_recipe=obj.id,
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Check if current recipe is in shopping cart of a user."""
        request = self.context.get('request')
        if request:
            return ShoppingCart.objects.filter(
                user=request.user,
            ).filter(
                recipe_in_cart=obj.id,
            ).exists()
        return False


class PostRecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for Recipe model."""

    ingredients = IngredientRecipeSerializer(required=False, many=True)
    # image = Base64ImageField(required=True)
    text = serializers.CharField(source='description')

    class Meta:
        """Describe settings for RecipeSerializer."""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            # 'image',
            'name',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        """Define a way how Recipe instance is create."""
        ingredients = validated_data.pop('ingredients')
        # tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        if not ingredients:
            return recipe

        for ingredient in ingredients:
            if Ingredient.objects.get(id=ingredient.id):
                IngredientRecipe.objects.get_or_create(
                    ingredient=ingredient,
                    recipe=recipe,
                    quantity=ingredient.amount,
                )

'''
        for tag in tags:
            if Tag.objects.get(tag):
                TagRecipe.objects.get_or_create(
                    tag=tag,
                    recipe=recipe,
                )
'''

