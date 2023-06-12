from django.contrib import admin

from recipes.models import Recipe, Tag, Ingridient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin panel settings for Recipe model."""

    list_display = (
        'author',
        'name',
        'description',
        'cooking_time',
        'get_ingridients',
        'get_tags',
    )
    search_fields = list_display
    list_filter = ('author', 'ingridients', 'tags')
    empty_value_display = '-empty-'
    list_editable = ('name', 'description', 'cooking_time')

    def get_ingridients(self, obj):
        """Collect all ingridients and return a string of them."""
        return '|'.join([ingridient.name for ingridient in obj.ingridients.all()])

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


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    """Admin panel settings for Tag model."""

    list_display = (
        'name',
        'measure',
    )
    search_fields = list_display
    list_filter = ('measure',)
    empty_value_display = '-empty-'
    list_editable = list_display
    list_display_links = None
