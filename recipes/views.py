from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category
from .forms import RecipeForm, RecipeImageFormset


def home_page(request):
    return render(request, 'recipes/home.html')


def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query) if query else Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


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
    category_obj = get_object_or_404(Category, name__iexact=category)  # Get the Category object
    recipes = Recipe.objects.filter(category=category_obj)  # Filter recipes by the category object
    return render(request, "recipes/recipe_list.html", {"recipes": recipes, "category": category})


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect("recipes:recipe_list")


def about_page(request):
    return render(request, "recipes/about.html")
