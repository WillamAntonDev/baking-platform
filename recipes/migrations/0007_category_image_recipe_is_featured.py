# Generated by Django 5.1.4 on 2025-01-09 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_alter_category_slug_alter_recipe_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="categories/"),
        ),
        migrations.AddField(
            model_name="recipe",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
    ]