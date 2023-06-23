"""Модуль содержит фильтры для приложения api."""
from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтрует произведения по полям."""

    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="exact")
    author = filters.CharFilter(field_name="author__id", lookup_expr="exact")


class Meta:
    """Определяет настройки фильтра TitleFilter."""

    model = Recipe
    fields = ['tags', 'author']
