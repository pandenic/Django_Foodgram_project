from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

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
