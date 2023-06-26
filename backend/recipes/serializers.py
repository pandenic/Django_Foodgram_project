"""Describe custom serializers for the recipes app."""
import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientRecipe
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
        if 'current_recipe_id' not in self.context:
            return None
        ingredient_recipe = IngredientRecipe.objects.get(
            ingredient=obj.id,
            recipe=self.context['current_recipe_id'],
        )
        return ingredient_recipe.quantity


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serialize requests for Ingredients model."""

    id = serializers.IntegerField(read_only=False)
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        """Describe settings for IngredientSerializer."""

        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, value):
        if value <= 0 or value is None:
            raise serializers.ValidationError({'amount': Errors.WRONG_INGREDIENTS_AMOUNT})
        return value

    def validate_id(self, value):
        get_object_or_404(Ingredient, id=value)
        return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GetRecipeSerializer(serializers.ModelSerializer):
    """Serialize GET request for Recipe model."""

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
            #'image',
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

    def get_ingredients(self, obj):
        return IngredientSerializer(
            obj.ingredients.all(),
            many=True,
            context={'current_recipe_id': obj.id}
        ).data


class PostRecipeSerializer(serializers.ModelSerializer):
    """Serialize POST request for Recipe model."""

    tags = serializers.PrimaryKeyRelatedField(
        read_only=False,
        required=True,
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(many=True, required=True, source='ingredient_recipe')
    text = serializers.CharField(source='description')
    #image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        """Describe settings for RecipeSerializer."""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            #'image',
            'name',
            'text',
            'cooking_time',
        )

    def add_ingredients(self, recipe, ingredients):
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
        #instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

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

    class Meta:

        model = Recipe
        fields = (
            'id',
            'name',
            #'image',
            'cooking_time',
        )
