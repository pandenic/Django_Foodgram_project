"""Describe custom serializers for the users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Follow

User = get_user_model()


class GetUserSerializer(serializers.ModelSerializer):
    """Serialize get request for User model."""

    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254,
    )

    class Meta:
        """Describe settings for GetUserSerializer."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Check if current user follow this user."""
        request = self.context.get('request')
        if request:
            return Follow.objects.filter(
                follower=request.user.id,
            ).filter(
                following=obj.id,
            ).exists()
        return False


class PostUserSerializer(serializers.ModelSerializer):
    """Serialize User model on post request."""

    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254,
    )

    class Meta:
        """Describe settings for PostUserSerializer."""

        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def to_representation(self, data):
        return {
            'email': data.email,
            'id': data.id,
            'username': data.username,
            'first_name': data.first_name,
            'last_name': data.last_name,
        }

    def validate(self, attrs):
        """Validate serialized data of UserSerializer."""
        for attr, value in attrs.items():
            if not value:
                raise serializers.ValidationError({attr: 'Обязательное поле.'})
        return attrs


class SetPasswordSerializer(serializers.ModelSerializer):
    """Serialize set password action."""

    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(
        source='password',
        max_length=150,
    )

    class Meta:
        """Describe settings for SetPasswordSerializer."""

        model = User
        fields = (
            'new_password',
            'current_password',
        )

    def validate_current_password(self, value):
        """Check if current password is correct."""
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError({'current_password': 'Пароль неверный'})
        return value


class GetTokenSerializer(serializers.Serializer):
    """Serialize token obtain."""

    password = serializers.CharField(max_length=150)
    email = serializers.EmailField()

'''
class SubscriptionSerializer(GetUserSerializer):
    """Serialize subscription process."""

    class Meta:
        """Describe settings for SubscriptionSerializer."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
'''