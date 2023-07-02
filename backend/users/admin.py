from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin panel settings for User model."""

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', )
    list_filter = ('email', 'username')
    empty_value_display = '-empty-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Follow panel settings for User model."""

    list_display = (
        'id',
        'follower',
        'following',
    )
    search_fields = list_display
    list_filter = list_display
    empty_value_display = '-empty-'

