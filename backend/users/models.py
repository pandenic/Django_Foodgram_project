from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Override the User model to change settings."""


    class Meta:
        """Change a behavior of the Ingredient model fields."""

        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'
