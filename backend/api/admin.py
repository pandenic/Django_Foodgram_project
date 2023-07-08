"""Decribe admin panel settings."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import transaction

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag, TagRecipe)
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
    search_fields = ('username',)
    list_filter = ('email', 'username')
    empty_value_display = '-empty-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin panel settings for Follow model."""

    list_display = (
        'id',
        'follower_username',
        'follower_email',
        'following_username',
        'following_email',
    )
    search_fields = (
        'follower__username',
        'follower__email',
        'following__username',
        'following__email',
    )
    empty_value_display = '-empty-'

    def follower_username(self, obj):
        """Represent a username field from User model."""
        return obj.follower.username

    def follower_email(self, obj):
        """Represent an email field from User model."""
        return obj.follower.email

    def following_username(self, obj):
        """Represent a username field from User model."""
        return obj.following.username

    def following_email(self, obj):
        """Represent an email field from User model."""
        return obj.following.email


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    """Admin panel settings for Favorite model."""

    list_display = (
        'id',
        'favorite_recipe',
        'username',
        'email',
        'tags',
    )
    search_fields = ('user__username', 'user__email', 'favorite_recipe__name')
    list_filter = ('favorite_recipe__tags',)
    empty_value_display = '-empty-'

    def username(self, obj):
        """Represent a username field from User model."""
        return obj.user.username

    def email(self, obj):
        """Represent an email field from User model."""
        return obj.user.email

    def tags(self, obj):
        """Collect all tags and return a string of them."""
        return ' | '.join([tag.name for tag in obj.favorite_recipe.tags.all()])


class IngredientRecipeInline(admin.TabularInline):
    """Creates interface for ingredients in RecipeAdmin."""

    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.StackedInline):
    """Creates interface for tags in RecipeAdmin."""

    model = TagRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for Recipe model."""

    list_display = (
        'id',
        'name',
        'username',
        'email',
        'added_to_favorites',
        'ingredient_list',
        'tag_list',
    )
    inlines = (
        IngredientRecipeInline,
        TagRecipeInline,
    )
    search_fields = ('author__username', 'author__email', 'name')
    list_filter = ('tags',)
    empty_value_display = '-empty-'

    def added_to_favorites(self, obj):
        """Calculate how many users added a recipe to favorites."""
        return obj.favorited_by.count()

    def username(self, obj):
        """Represent a username field from User model."""
        return obj.author.username

    def email(self, obj):
        """Represent an email field from User model."""
        return obj.author.email

    def ingredient_list(self, obj):
        """Collect all ingredients and return a string of them."""
        return ' | '.join([ingredient.name for ingredient in obj.ingredients.all()])

    def tag_list(self, obj):
        """Collect all tags and return a string of them."""
        return ' | '.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'id',
        'name',
        'slug',
        'color',
    )
    search_fields = list_display
    list_filter = ('color',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin panel settings for Ingredient model."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = list_display
    list_filter = ('measurement_unit',)
    empty_value_display = '-empty-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for IngredientRecipe model."""

    list_display = (
        'id',
        'ingredient',
        'recipe',
        'quantity',
        'username',
        'email',
        'tags',
    )
    search_fields = (
        'recipe__author__username',
        'recipe__author__email',
        'ingredient__name',
        'recipe__name'
    )
    list_filter = ('recipe__tags',)
    empty_value_display = '-empty-'

    def username(self, obj):
        """Represent a username field from User model."""
        return obj.recipe.author.username

    def email(self, obj):
        """Represent an email field from User model."""
        return obj.recipe.author.email

    def tags(self, obj):
        """Collect all tags and return a string of them."""
        return ' | '.join([tag.name for tag in obj.recipe.tags.all()])


@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    """Admin panel settings for ShoppingCart model."""

    list_display = (
        'id',
        'recipe_in_cart',
        'username',
        'email',
        'tags',
    )
    search_fields = ('user__username', 'user__email', 'recipe_in_cart__name')
    list_filter = ('recipe_in_cart__tags',)
    empty_value_display = '-empty-'

    def username(self, obj):
        """Represent a username field from User model."""
        return obj.user.username

    def email(self, obj):
        """Represent an email field from User model."""
        return obj.user.email

    def tags(self, obj):
        """Collect all tags and return a string of them."""
        return ' | '.join([tag.name for tag in obj.recipe_in_cart.tags.all()])
