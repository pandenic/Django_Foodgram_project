"""Describe custom mixins for an Api app."""
from rest_framework import mixins, viewsets


class ListCreateRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Describe a custom ViewSet for List, Create and Retrieve methods."""

    pass
