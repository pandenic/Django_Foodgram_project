"""Describe custom views for the users app."""
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.mixins import ListCreateViewSet
from users.serializers import UserSerializer
from users.pagination import UserPagination

User = get_user_model()


class UserViewSet(ListCreateViewSet):
    """Perform CRUD operations for User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    @action(
        ('get',),
        detail=False,
    )
    def me(self, request):
        """Process './me' endpoint."""
        serializer = UserSerializer(request.user)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

