from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient, Favorite, IngredientRecipe, ShoppingCart


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'id',
        'favorite_recipe',
        'user',
    )
    search_fields = list_display
    list_filter = ('favorite_recipe', 'user')
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for Recipe model."""

    list_display = (
        'id',
        'name',
        'author',
        'get_tags',
        'added_to_favorites',
    )
    search_fields = list_display
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'

    def get_tags(self, obj):
        """Collect all tags and return a string of them."""
        return ' | '.join([tag.name for tag in obj.tags.all()])

    def added_to_favorites(self, obj):
        """Calculate how many users added a recipe to favorites."""
        return obj.favorited_by.count()


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
    """Admin panel settings for Tag model."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = list_display
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'id',
        'ingredient',
        'recipe',
        'quantity',
    )
    search_fields = list_display
    list_filter = ('ingredient', 'recipe')
    empty_value_display = '-empty-'


@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'id',
        'recipe_in_cart',
        'user',
    )
    search_fields = list_display
    list_filter = ('recipe_in_cart', 'user')
    empty_value_display = '-empty-'
