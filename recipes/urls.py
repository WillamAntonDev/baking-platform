from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),  # List of all recipes
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),  # Recipe details by primary key
    path("<int:id>/edit/", views.recipe_edit, name="recipe_edit"),  # Edit recipe by ID
    path("<int:id>/delete/", views.recipe_delete, name="recipe_delete"),  # Delete recipe by ID
    path("about/", views.about_page, name="about"),  # About page
    path("category/<slug:category>/", views.recipe_by_category, name="recipe_by_category"),

  # Recipes by category slug
]
