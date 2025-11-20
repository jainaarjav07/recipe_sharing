from django.contrib import admin
from .models import Recipe, Cookbook, MealPlan, NutritionInfo, RecipeSuggestion, FavoriteRecipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'difficulty', 'prep_time', 'cook_time', 'created_at']
    list_filter = ['difficulty', 'created_at', 'author']
    search_fields = ['title', 'description', 'ingredients']

@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'created_at']
    filter_horizontal = ['recipes']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'date', 'meal_type', 'servings']
    list_filter = ['date', 'meal_type']

@admin.register(NutritionInfo)
class NutritionInfoAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'calories_per_serving', 'protein', 'carbs', 'fat']

@admin.register(RecipeSuggestion)
class RecipeSuggestionAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'created_at']
    list_filter = ['created_at']

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']