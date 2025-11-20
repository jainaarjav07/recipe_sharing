from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipes/<int:pk>/scale/', views.scale_recipe, name='scale_recipe'),
    path('cookbooks/', views.cookbook_list, name='cookbook_list'),
    path('cookbooks/<int:pk>/', views.cookbook_detail, name='cookbook_detail'),
    path('cookbooks/create/', views.cookbook_create, name='cookbook_create'),
    path('meal-plan/', views.meal_plan, name='meal_plan'),
    path('recipes/<int:pk>/suggest/', views.add_suggestion, name='add_suggestion'),
    path('recipes/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('recipes/<int:recipe_pk>/add-to-cookbook/<int:cookbook_pk>/', views.add_to_cookbook, name='add_to_cookbook'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]