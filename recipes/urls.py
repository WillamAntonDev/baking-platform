from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("<int:id>/edit/", views.recipe_edit, name="recipe_edit"),
    path("<int:id>/delete/", views.recipe_delete, name="recipe_delete"),
    path("about/", views.about_page, name="about"),
    path("category/<str:category>/", views.recipe_by_category, name="category"),  # Add this line
]
