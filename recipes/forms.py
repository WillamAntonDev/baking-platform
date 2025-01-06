from django import forms
from .models import Recipe, RecipeImage
from django.forms.models import inlineformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image']
        
RecipeImageFormset = inlineformset_factory(Recipe, RecipeImage, fields=('image',), extra=3)
