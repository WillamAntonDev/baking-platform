from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories/images/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(
        upload_to="recipes/images/",
        blank=True,
        null=True,
        default="recipes/images/default-recipe.jpg"
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def main_image(self):
        # Prioritize RecipeImage main image
        main_image_obj = self.images.filter(is_main_image=True).first()
        if main_image_obj:
            return main_image_obj.image.url
        # Fallback to Recipe image field
        if self.image:
            return self.image.url
        # Default static image
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/')
    is_main_image = models.BooleanField(default=False)  # Field to mark the main image

    def save(self, *args, **kwargs):
        # Ensure only one image is the main image per recipe
        if self.is_main_image:
            RecipeImage.objects.filter(recipe=self.recipe, is_main_image=True).update(is_main_image=False)
        
        super().save(*args, **kwargs)  # Save the image first
        RecipeImage.fix_image_orientation(self.image.path)  # Fix orientation after saving

    @staticmethod
    def fix_image_orientation(image_path):
        try:
            img = Image.open(image_path)
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif = img._getexif()
            if exif and orientation in exif:
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
            img = img.convert("RGB")
            img.thumbnail((800, 800))  # Resize image to 800x800 max
            img.save(image_path, quality=85)  # Save with optimized quality
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    def __str__(self):
        return f"{self.recipe.title} - {'Main Image' if self.is_main_image else 'Additional Image'}"
