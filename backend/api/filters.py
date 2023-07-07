"""Describe filters for an Api app."""
from django.contrib.auth import get_user_model
from django_filters import rest_framework as df
from rest_framework import filters

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(df.FilterSet):
    """Describe settings of recipe filtration."""

    tags = df.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = df.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
    )
    is_favorited = df.BooleanFilter(
        field_name='favorited_by__user',
        method='filter_user_lists',
    )
    is_in_shopping_cart = df.BooleanFilter(
        field_name='added_to_cart__user',
        method='filter_user_lists',
    )

    def filter_user_lists(self, queryset, name, value):
        """Change behavior of a filter.

        Depend on is_in_shopping_cart query param value.
        """
        if value:
            return queryset.filter(**{name: self.request.user})
        return queryset.exclude(**{name: self.request.user})

    class Meta:
        """Define settings of RecipeFilter."""

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')


class IngredientSearchFilter(filters.SearchFilter):
    """Describe settings of ingredient filtration."""

    search_param = 'name'
