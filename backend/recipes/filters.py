"""Модуль содержит фильтры для приложения api."""
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    """Фильтрует произведения по полям."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorited_by__user',
        method='filter_user_lists',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='added_to_cart__user',
        method='filter_user_lists',
    )

    def filter_user_lists(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})
        return queryset.exclude(**{name: self.request.user})


class Meta:
    """Определяет настройки фильтра TitleFilter."""

    model = Recipe
    fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
