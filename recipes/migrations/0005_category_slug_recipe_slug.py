from django.db import migrations, models
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    Category = apps.get_model('recipes', 'Category')
    Recipe = apps.get_model('recipes', 'Recipe')

    for category in Category.objects.all():
        if not category.slug:
            slug = slugify(category.name)
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{slugify(category.name)}-{counter}"
                counter += 1
            category.slug = slug
            category.save()

    for recipe in Recipe.objects.all():
        if not recipe.slug:
            slug = slugify(recipe.title)
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{slugify(recipe.title)}-{counter}"
                counter += 1
            recipe.slug = slug
            recipe.save()

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_category_name_alter_recipe_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.RunPython(populate_slugs),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
