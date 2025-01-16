from django.contrib import admin
from .models import Recipe, RecipeImage, Category

# Inline admin for RecipeImage to manage images directly from the Recipe admin page
class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1  # Number of empty forms for adding new images
    fields = ('image', 'is_main_image')  # Include is_main_image in the inline admin
    readonly_fields = ('id',)  # Optional: make ID read-only for better clarity
    show_change_link = True  # Allow links to detailed editing

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug based on title
    inlines = [RecipeImageInline]  # Add RecipeImage inline to Recipe admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'image', 'is_main_image')  # Include is_main_image
    list_editable = ('is_main_image',)  # Allow direct editing of is_main_image
    list_filter = ('is_main_image', 'recipe')  # Filters for better navigation
    search_fields = ('recipe__title',)  # Search RecipeImage by recipe title
