#!/usr/bin/env python3
"""
Setup script for Recipe Community project
"""
import os
import sys
import subprocess

def run_command(command, description):
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🍳 Setting up Recipe Community Project\n")
    
    # Install dependencies
    if not run_command("pip3 install Django django-crispy-forms crispy-bootstrap5 Pillow requests", 
                      "Installing dependencies"):
        return
    
    # Run migrations
    if not run_command("python3 manage.py migrate", "Running database migrations"):
        return
    
    # Create superuser if it doesn't exist
    run_command("echo \"from django.contrib.auth.models import User; User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_superuser': True, 'is_staff': True})\" | python3 manage.py shell", 
               "Creating admin user")
    
    # Populate sample data
    run_command("python3 manage.py populate_sample_data", "Adding sample recipes")
    
    print("\n🎉 Setup complete!")
    print("📝 Admin login: admin/admin123")
    print("👤 Demo user: demo/demo123")
    print("🚀 Run: python3 manage.py runserver")

if __name__ == '__main__':
    main()