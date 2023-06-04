from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.pagination import UserPagination

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Perform CRUD operations for User model."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def me(self, request):
        """Process 'users/me' endpoint."""
        serializer = UserSerializer(request.user)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
