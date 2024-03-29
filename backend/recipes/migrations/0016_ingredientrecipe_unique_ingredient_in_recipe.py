# Generated by Django 4.2.1 on 2023-07-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0015_alter_ingredientrecipe_quantity'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_in_recipe',
            ),
        ),
    ]
