#!/usr/bin/env python3
"""
Quick server startup script for Recipe Community
"""
import os
import sys
import subprocess

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_community.settings')
    
    print("🍳 Starting Recipe Community Server...")
    print("📝 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("🏠 Home: http://127.0.0.1:8000/")
    print("👤 Demo User: demo/demo123")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    main()