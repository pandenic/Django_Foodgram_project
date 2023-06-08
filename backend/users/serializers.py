"""Describe custom serializers for the users app."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
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

    def to_representation(self, data):
        representation = {
            'email': data.email,
            'id': data.id,
            'username': data.username,
            'first_name': data.first_name,
            'last_name': data.last_name,
        }
        if self.context['request'].method == 'POST':
            representation['is_subscribed'] = self.is_subscribed
        return representation


class SetPasswordSerializer(serializers.Serializer):
    """Serialize set password action."""

    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate_current_password(self, value):
        """Check if current password is correct."""
        user = self.context['request'].user
        if not user.check_password(self.current_password):
            raise serializers.ValidationError({'current_password': 'Пароль неверный'})
        return value


class GetTokenSerializer(serializers.Serializer):
    """Serialize token obtain."""

    password = serializers.CharField(max_length=150)
    email = serializers.EmailField()


