"""Describe custom serializers for the recipes app."""
from rest_framework import serializers

from recipes.models import Tag, Ingredient


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
