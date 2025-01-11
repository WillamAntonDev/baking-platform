from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="categories/images/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(
        upload_to="recipes/images/",
        blank=True,
        null=True,
        default="recipes/images/default-recipe.jpg"  # Add a default image path
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Resize the image if it exists
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))
            img.save(self.image.path)

    def __str__(self):
        return self.title

class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='recipes/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            max_size = (800, 800)
            img.thumbnail(max_size)
            img.save(self.image.path)
