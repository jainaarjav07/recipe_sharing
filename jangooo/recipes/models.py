from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=4)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

class Cookbook(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    recipes = models.ManyToManyField(Recipe, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class MealPlan(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    servings = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['user', 'date', 'meal_type', 'recipe']
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} - {self.date}"

class NutritionInfo(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    calories_per_serving = models.PositiveIntegerField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True, help_text="Grams per serving")
    carbs = models.FloatField(null=True, blank=True, help_text="Grams per serving")
    fat = models.FloatField(null=True, blank=True, help_text="Grams per serving")
    fiber = models.FloatField(null=True, blank=True, help_text="Grams per serving")
    
    def __str__(self):
        return f"Nutrition for {self.recipe.title}"

class RecipeSuggestion(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Suggestion by {self.user.username} for {self.recipe.title}"

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'recipe']
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"