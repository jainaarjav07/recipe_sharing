# Recipe Community - Deployment Guide

## Quick Start

1. **Setup Project:**
   ```bash
   python3 setup.py
   ```

2. **Start Server:**
   ```bash
   python3 run_server.py
   # OR
   python3 manage.py runserver
   ```

3. **Access Application:**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Default Accounts

- **Admin:** admin / admin123
- **Demo User:** demo / demo123

## Features Available

✅ **Recipe Management**
- Create, edit, delete recipes
- Image upload support
- Recipe scaling by servings

✅ **User Authentication**
- Registration and login
- Personal recipe management

✅ **Cookbooks**
- Create custom recipe collections
- Organize favorite recipes

✅ **Meal Planning**
- Plan meals by date and type
- Track servings

✅ **Nutritional Information**
- Optional nutrition data per recipe

✅ **API Integration Ready**
- Structure for external recipe APIs
- Ingredient substitution support

## Production Deployment

1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend
5. Set secure secret key
6. Enable HTTPS