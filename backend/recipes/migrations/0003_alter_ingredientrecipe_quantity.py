# Generated by Django 4.2.1 on 2023-06-19 17:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='quantity',
            field=models.IntegerField(help_text='Содержит количество ингридиента', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество ингридиента'),
        ),
    ]
