"""Describe custom views for the users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.mixins import ListCreateViewSet, ListViewSet
from users.serializers import GetUserSerializer, PostUserSerializer, SetPasswordSerializer, GetTokenSerializer
from users.pagination import UserPagination

User = get_user_model()


class UserViewSet(ListCreateViewSet):
    """Perform GET and POST operations for User model."""

    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = UserPagination
    permission_classes = (permissions.AllowAny,)

    @action(
        ('get',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Process './me' endpoint."""
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ('post',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        """Process './set_password' endpoint."""
        serializer = SetPasswordSerializer(
            request.user,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            password=make_password(
                serializer.validated_data['new_password']
            )
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """Perform actions during save an instance of user."""
        serializer.save(
            password=make_password(serializer.validated_data['password']),
        )

    def get_serializer_class(self):
        """Choose serializer class depend on method."""
        if self.action == 'list':
            return GetUserSerializer
        return PostUserSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    """Obtain token for user."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    user = get_object_or_404(User, email=email)

    password = serializer.validated_data['password']
    if not check_password(password, user.password):
        return Response(
            {'password': 'Пароль неверный'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = Token.objects.create(user=user)

    return Response(
        {'auth_token': str(token.key)},
        status=status.HTTP_201_CREATED,
    )


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def delete_token(request):
    """Delete token for user."""
    token = get_object_or_404(Token, user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(ListViewSet):
    """Show subscriptions for a certain user."""

    def get_queryset(self):
        """Define queryset for a certain user."""
        pass


