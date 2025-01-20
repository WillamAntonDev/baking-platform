from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Recipe, Category
from .forms import RecipeForm, RecipeImageFormset

# Constant for pagination
RECIPES_PER_PAGE = 6

# Helper function to verify if the user is Holly
def is_holly(user):
    return user.username == "hollyanton"

# Helper function to filter and order recipes
def get_filtered_recipes(queryset, search_query=None):
    if search_query:
        return queryset.filter(title__icontains=search_query).order_by('-created_at')
    return queryset.order_by('-created_at')

# Home Page View
def home(request):
    recipes = get_filtered_recipes(Recipe.objects.all())
    return render(request, 'home.html', {'recipes': recipes})

# Recipe List View
def recipe_list(request):
    search_query = request.GET.get('q')
    recipes = get_filtered_recipes(Recipe.objects.all(), search_query)
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all().order_by('name')

    return render(request, 'recipes/recipe_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

# Recipe Detail View
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    steps = recipe.instructions.splitlines()  # Split instructions into steps
    images = recipe.images.order_by('step_number')  # Order images by step number
    zipped_steps_and_images = zip(steps, images)  # Pair steps with images

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'zipped_steps_and_images': zipped_steps_and_images,
    })

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
    recipes = get_filtered_recipes(Recipe.objects.filter(category=category))
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipes_by_category.html', {
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
