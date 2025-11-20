from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Cookbook, NutritionInfo

class Command(BaseCommand):
    help = 'Populate database with sample recipes'

    def handle(self, *args, **options):
        # Create sample user if doesn't exist
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@example.com', 'first_name': 'Demo', 'last_name': 'User'}
        )
        if created:
            user.set_password('demo123')
            user.save()

        # Sample recipes
        recipes_data = [
            {
                'title': 'Classic Chocolate Chip Cookies',
                'description': 'Soft and chewy chocolate chip cookies that everyone loves.',
                'ingredients': '''2 1/4 cups all-purpose flour
1 tsp baking soda
1 tsp salt
1 cup butter, softened
3/4 cup granulated sugar
3/4 cup brown sugar
2 large eggs
2 tsp vanilla extract
2 cups chocolate chips''',
                'instructions': '''1. Preheat oven to 375°F.
2. Mix flour, baking soda, and salt in a bowl.
3. Cream butter and sugars until fluffy.
4. Beat in eggs and vanilla.
5. Gradually add flour mixture.
6. Stir in chocolate chips.
7. Drop rounded tablespoons onto ungreased baking sheets.
8. Bake 9-11 minutes until golden brown.''',
                'prep_time': 15,
                'cook_time': 10,
                'servings': 24,
                'difficulty': 'easy'
            },
            {
                'title': 'Spaghetti Carbonara',
                'description': 'Authentic Italian pasta dish with eggs, cheese, and pancetta.',
                'ingredients': '''1 lb spaghetti
6 oz pancetta, diced
4 large eggs
1 cup Parmesan cheese, grated
2 cloves garlic, minced
Salt and black pepper to taste
2 tbsp olive oil''',
                'instructions': '''1. Cook spaghetti according to package directions.
2. Cook pancetta until crispy.
3. Whisk eggs with Parmesan and pepper.
4. Drain pasta, reserving 1 cup pasta water.
5. Toss hot pasta with pancetta and garlic.
6. Remove from heat, add egg mixture, toss quickly.
7. Add pasta water if needed for creaminess.
8. Serve immediately with extra Parmesan.''',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'medium'
            }
        ]

        for recipe_data in recipes_data:
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                author=user,
                defaults=recipe_data
            )
            if created:
                self.stdout.write(f'Created recipe: {recipe.title}')

        # Create sample cookbook
        cookbook, created = Cookbook.objects.get_or_create(
            name='My Favorites',
            author=user,
            defaults={'description': 'Collection of my favorite recipes'}
        )
        if created:
            cookbook.recipes.set(Recipe.objects.filter(author=user))
            self.stdout.write('Created sample cookbook')

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))