"""Describe custom pagination classes for recipes app."""
from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Describe custom settings for UserPagination."""

    page_size_query_param = 'limit'
