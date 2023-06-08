"""Describe custom views for the users app."""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions, serializers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.mixins import ListCreateViewSet
from users.serializers import PostUserSerializer, GetUserSerializer, SetPasswordSerizlizer, GetTokenSerializer
from users.pagination import UserPagination

User = get_user_model()


class UserViewSet(ListCreateViewSet):
    """Perform CRUD operations for User model."""

    queryset = User.objects.all()
    serializer_class = GetUserSerializer
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
        serializer = SetPasswordSerizlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        """Функция определяет сериалайзер в зависимости от метода."""
        if self.action == "list":
            return GetUserSerializer
        return PostUserSerializer


@api_view(('POST',))
def get_token(request):
    """An obtain token function."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = get_object_or_404(User, email=email)
    if not user.check_password(password):
        raise serializers.ValidationError({'password': 'Пароль неверный'})

    token = RefreshToken.for_user(user)
    return Response(
        {"auth_token": str(token.access_token)},
        status=status.HTTP_201_CREATED,
    )