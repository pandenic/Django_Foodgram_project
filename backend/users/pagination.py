"""Describe custom pagination classes."""
from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Describe custom settings for UserPagination."""

    page_size_query_param = 'limit'
