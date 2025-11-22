"""
Main entry point for Google App Engine
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app, init_db

# Initialize database only once (Gunicorn will handle this better)
# The app will initialize the database on first request if needed
try:
    with app.app_context():
        init_db()
except Exception as e:
    # Ignore if database already exists (from another worker)
    print(f"Database initialization: {e}")

# This is used by App Engine
if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
