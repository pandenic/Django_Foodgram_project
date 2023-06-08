"""Describe custom serializers for the users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from recipes.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serialize User model."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Describe settings for UserSerializer."""

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


class SetPasswordSerizlizer(serializers.Serializer):
    """Serialize set password action."""

    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)
