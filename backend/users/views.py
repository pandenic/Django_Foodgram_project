"""Describe custom views for the users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions, serializers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.mixins import ListCreateViewSet
from users.serializers import UserSerializer, SetPasswordSerializer, GetTokenSerializer
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
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Process './me' endpoint."""
        serializer = UserSerializer(request.user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)

    @action(
        ('post',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        """Process './set_password' endpoint."""
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """Perform actions during save an instance of user."""
        serializer.save(
            password=make_password(self.request.user),
        )


@api_view(('POST',))
def get_token(request):
    """An obtain token function."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = get_object_or_404(User, email=email)

    if not check_password(password, user.password):
        raise serializers.ValidationError({'password': f'Пароль неверный {user.password}'})

    token = RefreshToken.for_user(user)
    return Response(
        {"auth_token": str(token.access_token)},
        status=status.HTTP_201_CREATED,
    )