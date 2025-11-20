from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Recipe, Cookbook, MealPlan, NutritionInfo, RecipeSuggestion, FavoriteRecipe
from .forms import RecipeForm, CookbookForm, MealPlanForm, RecipeSuggestionForm, RecipeFilterForm
import requests
import json

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        form = RecipeFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['author']:
                queryset = queryset.filter(author=form.cleaned_data['author'])
            if form.cleaned_data['difficulty']:
                queryset = queryset.filter(difficulty=form.cleaned_data['difficulty'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RecipeFilterForm(self.request.GET)
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['nutrition'] = self.object.nutritioninfo
        except NutritionInfo.DoesNotExist:
            context['nutrition'] = None
        
        context['suggestions'] = self.object.suggestions.all()[:5]
        context['suggestion_form'] = RecipeSuggestionForm()
        
        if self.request.user.is_authenticated:
            context['is_favorite'] = FavoriteRecipe.objects.filter(
                user=self.request.user, recipe=self.object
            ).exists()
            context['user_cookbooks'] = Cookbook.objects.filter(author=self.request.user)
        
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

@login_required
def cookbook_list(request):
    cookbooks = Cookbook.objects.filter(author=request.user)
    return render(request, 'recipes/cookbook_list.html', {'cookbooks': cookbooks})

@login_required
def cookbook_detail(request, pk):
    cookbook = get_object_or_404(Cookbook, pk=pk, author=request.user)
    return render(request, 'recipes/cookbook_detail.html', {'cookbook': cookbook})

@login_required
def cookbook_create(request):
    if request.method == 'POST':
        form = CookbookForm(request.POST)
        if form.is_valid():
            cookbook = form.save(commit=False)
            cookbook.author = request.user
            cookbook.save()
            form.save_m2m()
            messages.success(request, 'Cookbook created successfully!')
            return redirect('cookbook_detail', pk=cookbook.pk)
    else:
        form = CookbookForm()
    return render(request, 'recipes/cookbook_form.html', {'form': form})

@login_required
def meal_plan(request):
    meal_plans = MealPlan.objects.filter(user=request.user).order_by('date', 'meal_type')
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            messages.success(request, 'Meal added to plan!')
            return redirect('meal_plan')
    else:
        form = MealPlanForm()
    return render(request, 'recipes/meal_plan.html', {'meal_plans': meal_plans, 'form': form})

def scale_recipe(request, pk):
    from .utils import scale_ingredient_line
    
    recipe = get_object_or_404(Recipe, pk=pk)
    servings = int(request.GET.get('servings', recipe.servings))
    scale_factor = servings / recipe.servings
    
    scaled_ingredients = []
    for line in recipe.ingredients.split('\n'):
        if line.strip():
            scaled_ingredients.append(scale_ingredient_line(line, scale_factor))
    
    return JsonResponse({
        'scaled_ingredients': '\n'.join(scaled_ingredients),
        'servings': servings,
        'prep_time': recipe.prep_time,
        'cook_time': recipe.cook_time
    })

def home(request):
    recent_recipes = Recipe.objects.all()[:6]
    return render(request, 'recipes/home.html', {'recent_recipes': recent_recipes})

@login_required
def add_suggestion(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.recipe = recipe
            suggestion.user = request.user
            suggestion.save()
            messages.success(request, 'Suggestion added successfully!')
    return redirect('recipe_detail', pk=pk)

@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    favorite, created = FavoriteRecipe.objects.get_or_create(
        user=request.user, recipe=recipe
    )
    if not created:
        favorite.delete()
        messages.success(request, 'Recipe removed from favorites!')
    else:
        messages.success(request, 'Recipe added to favorites!')
    return redirect('recipe_detail', pk=pk)

@login_required
def add_to_cookbook(request, recipe_pk, cookbook_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    cookbook = get_object_or_404(Cookbook, pk=cookbook_pk, author=request.user)
    cookbook.recipes.add(recipe)
    messages.success(request, f'Recipe added to {cookbook.name}!')
    return redirect('recipe_detail', pk=recipe_pk)

@login_required
def favorites_list(request):
    favorites = FavoriteRecipe.objects.filter(user=request.user)
    return render(request, 'recipes/favorites_list.html', {'favorites': favorites})