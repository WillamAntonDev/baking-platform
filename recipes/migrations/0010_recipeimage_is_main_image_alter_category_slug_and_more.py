# Generated by Django 5.1.4 on 2025-01-16 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0009_alter_recipe_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipeimage",
            name="is_main_image",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                blank=True, default="default-category-slug", unique=True
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="recipe",
            name="slug",
            field=models.SlugField(
                blank=True, default="default-category-slug", unique=True
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="recipeimage",
            name="image",
            field=models.ImageField(upload_to="recipe_images/"),
        ),
    ]
