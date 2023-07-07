# Generated by Django 4.2.1 on 2023-07-05 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0014_alter_ingredientrecipe_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='quantity',
            field=models.PositiveSmallIntegerField(
                help_text='Содержит количество ингридиента',
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name='Количество ингридиента',
            ),
        ),
    ]