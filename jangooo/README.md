# Recipe Sharing Community

A Django-based recipe sharing website where users can post recipes, create cookbooks, and plan meals.

## Features

- **Recipe Management**: Create, edit, and share recipes with images
- **Ingredient Scaling**: Automatically scale recipe ingredients based on servings
- **Cookbooks**: Organize recipes into custom cookbooks
- **Meal Planning**: Plan meals by date and meal type
- **Nutritional Information**: Track nutrition data for recipes
- **User Authentication**: Register, login, and manage personal recipes

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## Usage

- Visit the home page to see recent recipes
- Register an account to create and manage recipes
- Use the recipe scaling feature to adjust ingredient quantities
- Create cookbooks to organize your favorite recipes
- Plan meals using the meal planning feature

## Models

- **Recipe**: Core recipe model with ingredients, instructions, and metadata
- **Cookbook**: Collections of recipes
- **MealPlan**: Scheduled meals for specific dates
- **NutritionInfo**: Nutritional data for recipes

## API Integration Ready

The project structure supports future integration with recipe APIs for:
- Automatic nutritional information lookup
- Recipe suggestions
- Ingredient substitutions