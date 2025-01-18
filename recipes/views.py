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
    recipes = Recipe.objects.all().order_by('-created_at')  # Order recipes by creation date
    return render(request, 'home.html', {'recipes': recipes})


# Recipe List View
def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query).order_by('-created_at') if query else Recipe.objects.all().order_by('-created_at')
    paginator = Paginator(recipes, 6)  # Adjust number of recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all().order_by('name')  # Order categories alphabetically

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
    category = get_object_or_404(Category, slug=category)
    recipes = Recipe.objects.filter(category=category).order_by('-created_at')  # Order recipes in category
    paginator = Paginator(recipes, 6)  # Adjust number of recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_by_category.html', {
        'category': category,
        'page_obj': page_obj,
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
