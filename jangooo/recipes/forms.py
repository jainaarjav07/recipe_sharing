from django import forms
from django.contrib.auth.models import User
from .models import Recipe, Cookbook, MealPlan, RecipeSuggestion

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'prep_time', 
                 'cook_time', 'servings', 'difficulty', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Enter each ingredient on a new line'}),
            'instructions': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Enter step-by-step instructions'}),
            'prep_time': forms.NumberInput(attrs={'min': 1}),
            'cook_time': forms.NumberInput(attrs={'min': 1}),
            'servings': forms.NumberInput(attrs={'min': 1}),
        }

class CookbookForm(forms.ModelForm):
    class Meta:
        model = Cookbook
        fields = ['name', 'description', 'recipes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'recipes': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipes'].queryset = Recipe.objects.all()

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['recipe', 'date', 'meal_type', 'servings']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'servings': forms.NumberInput(attrs={'min': 1}),
        }

class RecipeSuggestionForm(forms.ModelForm):
    class Meta:
        model = RecipeSuggestion
        fields = ['suggestion']
        widgets = {
            'suggestion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your suggestion for this recipe...'})
        }

class RecipeFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=User.objects.filter(recipe__isnull=False).distinct(),
        required=False,
        empty_label="All Authors"
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'All Difficulties')] + Recipe.DIFFICULTY_CHOICES,
        required=False
    )