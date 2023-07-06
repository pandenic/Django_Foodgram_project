"""Describe constants which are used in a project."""
from foodgram.settings import (MAXIMUM_COOKING_TIME, MAXIMUM_INGREDIENT_AMOUNT,
                               MINIMUM_COOKING_TIME, MINIMUM_INGREDIENT_AMOUNT)


class HTTPMethods:
    """Contain constants for http methods."""

    DELETE = 'delete'
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'


class ErrorMessage:
    """Contain errors prompts."""

    NOTHING_TO_DELETE = 'Nothing to delete.'
    RECIPE_IN_FAVORITES = 'Recipe is in favorites already.'
    WRONG_INGREDIENTS_AMOUNT = (
        f'Wrong ingredients amount '
        f'(lower than {MINIMUM_INGREDIENT_AMOUNT} or '
        f'greater than {MAXIMUM_INGREDIENT_AMOUNT}).'
    )
    ALREADY_SUBSCRIBED = 'Already subscribed on author.'
    ALREADY_IN_SHOPPING_CART = 'Recipe is in shopping cart already.'
    CANNOT_FOLLOW_YOURSELF = 'You are cannot follow yourself.'
    WRONG_COOKING_TIME = (
        f'Wrong cooking time amount '
        f'(lower than {MINIMUM_COOKING_TIME} '
        f'or greater than {MAXIMUM_COOKING_TIME}).'
    )
    INGREDIENT_IS_NEED = 'At least one ingredient is needed.'
    MORE_THAN_ONE_INGREDIENT = (
        'Only one ingredient of exact type should be used'
    )
