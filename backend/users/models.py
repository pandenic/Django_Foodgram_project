from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Override the User model to change settings."""

    class Meta:
        """Change a behavior of the Ingredient model fields."""

        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Follow(models.Model):
    """Describe a model which stores follow - follower connection."""

    follower = models.ForeignKey(
        User,
        verbose_name='Follower',
        help_text='Follower who going to subscribe to author',
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        verbose_name='Following',
        help_text='Following who is followed by follower',
        on_delete=models.CASCADE,
        related_name='followings',
    )