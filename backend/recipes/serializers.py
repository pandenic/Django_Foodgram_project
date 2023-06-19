"""Describe custom serializers for the recipes app."""
import base64
from collections import OrderedDict

from django.core.files.base import ContentFile
from django.db.models import F
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


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize requests for Ingredients model."""

    id = serializers.IntegerField(read_only=False)
    amount = ReadWriteSerializerMethodField(method_name='get_amount')

    class Meta:
        """Describe settings for IngredientSerializer."""

        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        read_only_fields = ('name', 'measurement_unit')

    def get_amount(self, obj):
        if 'current_recipe_id' not in self.context:
            return None
        ingredient_recipe = IngredientRecipe.objects.get(
            ingredient=obj.id,
            recipe=self.context['current_recipe_id'],
        )
        return ingredient_recipe.quantity

    def to_representation(self, instance):
        result = super(IngredientSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    def validate_amount(self, value):
        if value['amount'] <= 0 or value['amount'] is None:
            raise serializers.ValidationError('Неверное количество ингредиентов')
        return value

    def create(self, validated_data):
        if 'amount' not in self.initial_data:
            raise serializers.ValidationError('No amount in validated date')
        ingredient_recipe_chain = IngredientRecipe.objects.get_or_create(
            ingredient_id=validated_data['id'],
            recipe_id=self.context['current_recipe_id'],
            quantity=validated_data['amount'],
        )
        return ingredient_recipe_chain


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for Recipe model."""

    ingredients = serializers.SerializerMethodField()
    author = GetUserSerializer(read_only=True)
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
             #'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'author',
            'is_favorited',
            'is_in_shopping_cart',

        )

    def create(self, validated_data):
        """Define a way how Recipe instance is create."""
        is_ingredients_in_data = 'ingredients' in self.initial_data
        is_tags_in_data = 'tags' in self.initial_data

        if is_tags_in_data:
            tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        if is_ingredients_in_data:
            ingredients = self.initial_data['ingredients']
            for ingredient in ingredients:
                ingredients_serializer = IngredientSerializer(data=ingredient, context={'current_recipe_id': recipe.id})
                ingredients_serializer.is_valid(raise_exception=True)
                ingredients_serializer.save()
        return recipe

    def get_ingredients(self, obj):
        return IngredientSerializer(obj.ingredients.all(), many=True).data

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

'''
class PostRecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for Recipe model."""

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
        is_ingredients_in_data = 'ingredients' in self.initial_data
        is_tags_in_data = 'tags' in self.initial_data

        if is_ingredients_in_data:
            ingredients = validated_data.pop('ingredients')
        if is_tags_in_data:
            tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        if is_ingredients_in_data:
            for ingredient in ingredients:
                current_ingredient = Ingredient.objects.get(
                    id=ingredient['id'])
                if current_ingredient:
                    IngredientRecipe.objects.get_or_create(
                        ingredient=current_ingredient,
                        recipe=recipe,
                        quantity=ingredient['quantity'],
                    )
        return recipe

    def to_representation(self, instance):
        """Define representation of PostRecipeSerializer."""
        representation = GetRecipeSerializer(instance)
        return representation.data
'''


'''
        for tag in tags:
            if Tag.objects.get(tag):
                TagRecipe.objects.get_or_create(
                    tag=tag,
                    recipe=recipe,
                )
'''

