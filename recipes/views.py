from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Recipe, Category
from .forms import RecipeForm, RecipeImageFormset


# Helper function to verify if the user is Holly
def is_holly(user):
    return user.username == "hollyanton"  # Update to match Holly's username


# Home Page View
def home(request):
    recent_recipes = Recipe.objects.order_by('-created_at')[:4]
    return render(request, 'home.html', {'recent_recipes': recent_recipes})

# Recipe List View
from django.core.paginator import Paginator

def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query) if query else Recipe.objects.all()
    paginator = Paginator(recipes, 6)  # Adjust number of recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    return render(request, 'recipes/recipe_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

# Recipe Detail View
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


# Recipe Edit View
@login_required
@user_passes_test(is_holly)
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    formset = RecipeImageFormset(request.POST or None, request.FILES or None, instance=recipe)

    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Recipe updated successfully.")
        return redirect('recipes:recipe_detail', pk=recipe.id)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset})

# Recipe by Category View
def recipe_by_category(request, category):
    category_obj = get_object_or_404(Category, slug=category)
    recipes = Recipe.objects.filter(category=category_obj)  # Fetch recipes for the category
    return render(request, "recipes/category.html", {
        "category": category_obj,
        "recipes": recipes,
    })


# Recipe Delete View
@login_required
@user_passes_test(is_holly)
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully.")
    return redirect("recipes:recipe_list")


# About Page View
def about_page(request):
    return render(request, "recipes/about.html")
