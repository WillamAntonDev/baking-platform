from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Recipe, Category
from .forms import RecipeForm, RecipeImageFormset


# Helper function to verify if the user is Holly
def is_holly(user):
    return user.username == "hollyanton"  # Replace with your wife's username


def home_page(request):
    featured_recipes = Recipe.objects.filter(is_featured=True)  # Recipes marked as featured
    categories = Category.objects.all()  # All categories
    return render(request, 'recipes/home.html', {
        'featured_recipes': featured_recipes,
        'categories': categories,
    })

def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query) if query else Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
@user_passes_test(is_holly)
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    form = RecipeForm(request.POST or None, instance=recipe)
    formset = RecipeImageFormset(request.POST or None, request.FILES or None, instance=recipe)

    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        return redirect('recipes:recipe_detail', pk=recipe.id)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset})


def recipe_by_category(request, category):
    category_obj = get_object_or_404(Category, slug=category)
    recipes = Recipe.objects.filter(category=category_obj)
    return render(request, "recipes/recipe_list.html", {"recipes": recipes, "category": category_obj})

@login_required
@user_passes_test(is_holly)
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect("recipes:recipe_list")


def about_page(request):
    return render(request, "recipes/about.html")
