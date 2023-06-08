"""Describe custom serializers for the users app."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Follow

User = get_user_model()


class GetUserSerializer(serializers.ModelSerializer):
    """Serialize User model on get request."""

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
        return Follow.objects.filter(
            follower=self.context['request'].user.id,
        ).filter(
            following=obj.id,
        ).exists()

    def validate(self, attrs):
        """Validate serialized data of UserSerializer."""
        for attr, value in attrs.items():
            if not value:
                raise serializers.ValidationError({attr: 'Обязательное поле.'})
        return attrs


class PostUserSerializer(serializers.ModelSerializer):
    """Serialize User model on post request."""

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
                'first_name': data.first_name,
                'last_name': data.last_name,
                'password': data.password,
            }


class SetPasswordSerizlizer(serializers.Serializer):
    """Serialize set password action."""

    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate_current_password(self, value):
        """Check if current password is correct."""
        if not self.context['request'].user.check_password(self.current_password):
            raise serializers.ValidationError('Пароль неверный')
        return value


class GetTokenSerializer(serializers.Serializer):
    """Serialize token obtain."""

    password = serializers.CharField(max_length=150)
    email = serializers.EmailField()


