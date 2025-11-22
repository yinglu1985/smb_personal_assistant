"""
Main entry point for Google App Engine
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app, init_db

# Initialize database on startup
with app.app_context():
    init_db()

# This is used by App Engine
if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
