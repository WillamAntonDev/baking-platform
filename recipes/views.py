from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm


def home_page(request):
    return render(request, "home.html")

# def recipe_create(request):
#     if request.method == "POST":
#         form = RecipeForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("recipes:recipe_list")
#     else:
#         form = RecipeForm()
#     return render(request, "recipes/recipe_form.html", {"form": form})

def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipes:recipe_detail", id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_form.html", {"form": form})

def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query) if query else Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, id):
    # Fetch a single recipe from the database
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})

def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect("recipes:recipe_list")

def about_page(request):
    return render(request, "about.html")
