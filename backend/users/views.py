"""Describe custom views for the users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipes.errors import ErrorMessage
from recipes.views import HTTPMethods
from users.mixins import ListCreateViewSet, ListViewSet
from users.models import Follow
from users.serializers import GetUserSerializer, PostUserSerializer, SetPasswordSerializer, GetTokenSerializer, \
    SubscriptionSerializer
from users.pagination import UserPagination

User = get_user_model()


class UserViewSet(ListCreateViewSet):
    """Perform GET and POST operations for User model."""

    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = UserPagination
    permission_classes = (permissions.AllowAny,)

    @action(
        (HTTPMethods.GET_LOWER,),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Process './me' endpoint."""
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        (HTTPMethods.POST_LOWER,),
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

    @action(
        (HTTPMethods.GET_LOWER,),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Process './subscriptions' endpoint."""
        subscriptions = User.objects.filter(followings__follower=request.user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request},
        )

        return self.get_paginated_response(serializer.data)

    @action(
        (HTTPMethods.POST_LOWER, HTTPMethods.DELETE_LOWER),
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk=None):
        """Process '.<id>/subscribe' endpoint."""
        user_to_follow = get_object_or_404(User, id=pk)
        follower_following_chain = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow,
        )

        if request.method == HTTPMethods.DELETE_UPPER and follower_following_chain:
            follower_following_chain.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethods.POST_UPPER and follower_following_chain:
            raise serializers.ValidationError({'errors': ErrorMessage.ALREADY_SUBSCRIBED})

        if request.method == HTTPMethods.DELETE_UPPER:
            raise serializers.ValidationError({'errors': ErrorMessage.NOTHING_TO_DELETE})

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow,
        )
        return Response(SubscriptionSerializer(user_to_follow).data, status=status.HTTP_201_CREATED)

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

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {'auth_token': token.key},
        status=status.HTTP_201_CREATED,
    )


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def delete_token(request):
    """Delete token for user."""
    token = get_object_or_404(Token, user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


