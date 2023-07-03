"""Describe custom pagination classes for an Api app."""
from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Describe custom settings for LimitPagination."""

    page_size_query_param = 'limit'
