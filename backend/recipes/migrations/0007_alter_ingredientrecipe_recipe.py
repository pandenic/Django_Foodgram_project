# Generated by Django 4.2.1 on 2023-06-22 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0006_alter_ingredientrecipe_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ingredient_recipe',
                to='recipes.recipe',
            ),
        ),
    ]
