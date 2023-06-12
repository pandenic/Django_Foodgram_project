"""Describe custom pagination classes for users app."""
from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Describe custom settings for UserPagination."""

    page_size_query_param = 'limit'
