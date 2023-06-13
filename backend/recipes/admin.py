from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for Recipe model."""

    list_display = (
        'author',
        'name',
        'description',
        'cooking_time',
        'get_ingredients',
        'get_tags',
    )
    search_fields = list_display
    list_filter = ('author', 'ingredients', 'tags')
    empty_value_display = '-empty-'
    list_editable = ('name', 'description', 'cooking_time')

    def get_ingredients(self, obj):
        """Collect all ingredients and return a string of them."""
        return '|'.join([ingredient.name for ingredient in obj.ingredients.all()])

    def get_tags(self, obj):
        """Collect all tags and return a string of them."""
        return '|'.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'name',
        'slug',
        'color',
    )
    search_fields = list_display
    list_filter = ('color',)
    empty_value_display = '-empty-'
    list_editable = list_display
    list_display_links = None


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = list_display
    list_filter = ('measurement_unit',)
    empty_value_display = '-empty-'
    list_editable = list_display
    list_display_links = None
