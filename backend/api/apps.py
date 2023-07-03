"""Describe Api app settings."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Config for Api app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
