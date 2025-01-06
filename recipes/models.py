from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Category model to represent different recipe categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensures each category name is unique

    def __str__(self):
        return self.name

# Recipe model to store recipes
class Recipe(models.Model):
    title = models.CharField(max_length=255)  # Title of the recipe
    ingredients = models.TextField()  # Ingredients listed as text
    instructions = models.TextField()  # Instructions for preparation
    image = models.ImageField(upload_to="recipes/images/", blank=True, null=True)  # Optional recipe image
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # If category is deleted, set the category field to NULL
        null=True,  # Allows NULL values in the database
        related_name='recipes'  # Allows reverse lookup (e.g., category.recipes.all())
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE  # Delete the recipe if the author is deleted
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date/time when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update date/time when the record is updated

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Custom save method to resize images before saving."""
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (800, 800)  # Resize to 800x800 pixels or smaller
            img.thumbnail(max_size)
            img.save(self.image.path)

# Model to handle additional images for recipes
class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,  # Delete all associated images if the recipe is deleted
        related_name='images'  # Allows reverse lookup (e.g., recipe.images.all())
    )
    image = models.ImageField(upload_to='recipes/')

    def save(self, *args, **kwargs):
        """Custom save method to resize images before saving."""
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (800, 800)  # Resize to 800x800 pixels
            img.thumbnail(max_size)
            img.save(self.image.path)
