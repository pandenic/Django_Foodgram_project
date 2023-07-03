"""Describe custom mixins for the users app."""
from rest_framework import mixins, viewsets


class ListCreateRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Describe a custom ViewSet for List, Create and Retrieve methods."""

    pass


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Describe a custom ViewSet for a List method."""

    pass
